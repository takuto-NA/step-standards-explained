<script setup>
import { onMounted, ref, onBeforeUnmount, reactive, watch, nextTick } from 'vue'

const container = ref(null)
const state = reactive({
  mode: 'curve', // 'curve' or 'surface'
  degree: 3,
  weight: 1.0,
  knot: 0.5,
  u: 0.5,
  v: 0.5,
  showPoints: true,
  showPolygon: true,
  showMesh: true,
})

let THREE, NURBSCurve, NURBSSurface, ParametricGeometry, OrbitControls;
let scene, camera, renderer, controls;
let curveMesh, surfaceMesh, pointMesh, lineGroup, markerPoint, uLine, vLine;
let animationId;

const initThree = async () => {
  THREE = await import('three')
  const curveMod = await import('three/addons/curves/NURBSCurve.js')
  const surfaceMod = await import('three/addons/curves/NURBSSurface.js')
  const geomMod = await import('three/addons/geometries/ParametricGeometry.js')
  const controlMod = await import('three/addons/controls/OrbitControls.js')
  
  NURBSCurve = curveMod.NURBSCurve
  NURBSSurface = surfaceMod.NURBSSurface
  ParametricGeometry = geomMod.ParametricGeometry
  OrbitControls = controlMod.OrbitControls

  if (!container.value) return

  const width = container.value.clientWidth
  const height = container.value.clientHeight

  scene = new THREE.Scene()
  scene.background = new THREE.Color(0x0f172a) // Slate 900

  camera = new THREE.PerspectiveCamera(50, width / height, 0.1, 1000)
  camera.position.set(4, 3, 6)

  renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true })
  renderer.setSize(width, height)
  renderer.setPixelRatio(window.devicePixelRatio)
  container.value.appendChild(renderer.domElement)

  controls = new OrbitControls(camera, renderer.domElement)
  controls.enableDamping = true

  // Lights
  const ambientLight = new THREE.AmbientLight(0xffffff, 0.7)
  scene.add(ambientLight)
  const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8)
  directionalLight.position.set(5, 10, 7.5)
  scene.add(directionalLight)

  // Marker for current U/V
  const markerGeom = new THREE.SphereGeometry(0.08, 16, 16)
  const markerMat = new THREE.MeshBasicMaterial({ color: 0x10b981 }) // Emerald 500
  markerPoint = new THREE.Mesh(markerGeom, markerMat)
  scene.add(markerPoint)

  updateNURBS()
  animate()
  
  window.addEventListener('resize', handleResize)
}

const updateNURBS = () => {
  if (!scene) return

  // Clear existing
  if (curveMesh) scene.remove(curveMesh)
  if (surfaceMesh) scene.remove(surfaceMesh)
  if (pointMesh) scene.remove(pointMesh)
  if (lineGroup) scene.remove(lineGroup)
  if (uLine) scene.remove(uLine)
  if (vLine) scene.remove(vLine)

  if (state.mode === 'curve') {
    renderCurve()
  } else {
    renderSurface()
  }
}

const renderCurve = () => {
  const points = [
    new THREE.Vector4(-3, 0, 0, 1),
    new THREE.Vector4(-1, 2, 0, 1),
    new THREE.Vector4(0, -1, 0, state.weight), // Center point with variable weight
    new THREE.Vector4(1, 2, 0, 1),
    new THREE.Vector4(3, 0, 0, 1)
  ]
  // Weighted coordinates for NURBSCurve (x*w, y*w, z*w, w)
  const weightedPoints = points.map(p => new THREE.Vector4(p.x * p.w, p.y * p.w, p.z * p.w, p.w))
  
  // Non-uniform knots
  const knots = [0, 0, 0, 0, state.knot, 1, 1, 1, 1]
  const curve = new NURBSCurve(state.degree, knots, weightedPoints)
  
  const geometry = new THREE.BufferGeometry().setFromPoints(curve.getPoints(100))
  const material = new THREE.LineBasicMaterial({ color: 0x3b82f6, linewidth: 3 }) // Blue 500
  curveMesh = new THREE.Line(geometry, material)
  scene.add(curveMesh)

  // Control polygon
  if (state.showPolygon) {
    const polyGeom = new THREE.BufferGeometry().setFromPoints(points.map(p => new THREE.Vector3(p.x, p.y, p.z)))
    const polyMat = new THREE.LineBasicMaterial({ color: 0x64748b, dashSize: 0.2, gapSize: 0.1 }) // Slate 500
    lineGroup = new THREE.Line(polyGeom, polyMat)
    scene.add(lineGroup)
  }

  // Control points
  if (state.showPoints) {
    const ptGeom = new THREE.BufferGeometry().setFromPoints(points.map(p => new THREE.Vector3(p.x, p.y, p.z)))
    const ptMat = new THREE.PointsMaterial({ color: 0xef4444, size: 0.15 }) // Red 500
    pointMesh = new THREE.Points(ptGeom, ptMat)
    scene.add(pointMesh)
  }

  // U marker
  const pos = curve.getPoint(state.u)
  markerPoint.position.copy(pos)
  markerPoint.visible = true
}

const renderSurface = () => {
  const nsControlPoints = []
  const weights = [
      [1, 1, 1, 1],
      [1, state.weight, state.weight, 1],
      [1, state.weight, state.weight, 1],
      [1, 1, 1, 1]
  ]
  
  for (let i = 0; i < 4; i++) {
    const row = []
    for (let j = 0; j < 4; j++) {
      const x = (i - 1.5) * 2
      const y = (j - 1.5) * 2
      let z = Math.sin(i) * Math.cos(j)
      if ((i === 1 || i === 2) && (j === 1 || j === 2)) z += 1.0;
      
      const w = weights[i][j]
      row.push(new THREE.Vector4(x * w, z * w, y * w, w))
    }
    nsControlPoints.push(row)
  }

  const knots1 = [0, 0, 0, 0, 1, 1, 1, 1]
  const knots2 = [0, 0, 0, 0, 1, 1, 1, 1]
  const nurbsSurface = new NURBSSurface(3, 3, knots1, knots2, nsControlPoints)

  const getSurfacePoint = (u, v, target) => {
    return nurbsSurface.getPoint(u, v, target)
  }

  const geometry = new ParametricGeometry(getSurfacePoint, 32, 32)
  const material = new THREE.MeshPhongMaterial({
    color: 0x3b82f6,
    side: THREE.DoubleSide,
    transparent: true,
    opacity: 0.7,
    flatShading: false,
    shininess: 100
  })
  surfaceMesh = new THREE.Mesh(geometry, material)
  if (state.showMesh) scene.add(surfaceMesh)

  // Wireframe
  const wireframeMaterial = new THREE.MeshBasicMaterial({ color: 0xffffff, wireframe: true, transparent: true, opacity: 0.1 })
  const wireframe = new THREE.Mesh(geometry, wireframeMaterial)
  surfaceMesh.add(wireframe)

  // Control points & polygon
  lineGroup = new THREE.Group()
  const ptCoords = []
  
  for (let i = 0; i < 4; i++) {
    const rowPoints = []
    for (let j = 0; j < 4; j++) {
      const p = nsControlPoints[i][j]
      const v3 = new THREE.Vector3(p.x / p.w, p.y / p.w, p.z / p.w)
      rowPoints.push(v3)
      ptCoords.push(v3.x, v3.y, v3.z)
    }
    if (state.showPolygon) {
      const rowGeom = new THREE.BufferGeometry().setFromPoints(rowPoints)
      lineGroup.add(new THREE.Line(rowGeom, new THREE.LineBasicMaterial({ color: 0x64748b, opacity: 0.4, transparent: true })))
    }
  }
  
  for (let j = 0; j < 4; j++) {
    const colPoints = []
    for (let i = 0; i < 4; i++) {
        const p = nsControlPoints[i][j]
        colPoints.push(new THREE.Vector3(p.x / p.w, p.y / p.w, p.z / p.w))
    }
    if (state.showPolygon) {
      const colGeom = new THREE.BufferGeometry().setFromPoints(colPoints)
      lineGroup.add(new THREE.Line(colGeom, new THREE.LineBasicMaterial({ color: 0x64748b, opacity: 0.4, transparent: true })))
    }
  }
  scene.add(lineGroup)

  if (state.showPoints) {
    const ptGeom = new THREE.BufferGeometry()
    ptGeom.setAttribute('position', new THREE.Float32BufferAttribute(ptCoords, 3))
    const ptMat = new THREE.PointsMaterial({ color: 0xef4444, size: 0.12 })
    pointMesh = new THREE.Points(ptGeom, ptMat)
    scene.add(pointMesh)
  }

  // U/V marker
  const pos = new THREE.Vector3()
  nurbsSurface.getPoint(state.u, state.v, pos)
  markerPoint.position.copy(pos)
  markerPoint.visible = true
}

const animate = () => {
  animationId = requestAnimationFrame(animate)
  if (controls) controls.update()
  if (renderer && scene && camera) renderer.render(scene, camera)
}

const handleResize = () => {
  if (!container.value || !renderer) return
  const width = container.value.clientWidth
  const height = container.value.clientHeight
  camera.aspect = width / height
  camera.updateProjectionMatrix()
  renderer.setSize(width, height)
}

watch(() => [state.mode, state.weight, state.knot, state.u, state.v, state.showPoints, state.showPolygon, state.showMesh], () => {
  updateNURBS()
})

onMounted(() => {
  initThree()
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', handleResize)
  cancelAnimationFrame(animationId)
  if (renderer) renderer.dispose()
})

const getKnotVector = computed(() => {
    if (state.mode === 'curve') {
        return `[0, 0, 0, 0, ${state.knot.toFixed(2)}, 1, 1, 1, 1]`;
    } else {
        return `U: [0, 0, 0, 0, 1, 1, 1, 1]\nV: [0, 0, 0, 0, 1, 1, 1, 1]`;
    }
})

const getStepSnippet = computed(() => {
    if (state.mode === 'curve') {
        return `#10 = B_SPLINE_CURVE_WITH_KNOTS('Curve', 3, (#1,#2,#3,#4,#5), .UNSPECIFIED., .F., .F., (4,1,4), (0.0, ${state.knot.toFixed(2)}, 1.0), .PIECEWISE_BEZIER_KNOTS.);\n#11 = RATIONAL_B_SPLINE_CURVE('', ..., (1.0, 1.0, ${state.weight.toFixed(2)}, 1.0, 1.0));`;
    } else {
        return `#20 = B_SPLINE_SURFACE_WITH_KNOTS('Surface', 3, 3, ((#1...),(...)), ...);`;
    }
})

</script>

<template>
  <div class="nurbs-viewer-wrapper">
    <div class="viewer-container">
      <div ref="container" class="canvas-container"></div>
      
      <!-- Overlay controls -->
      <div class="overlay-controls">
        <div class="control-group tabs">
          <button :class="{ active: state.mode === 'curve' }" @click="state.mode = 'curve'">Curve C(u)</button>
          <button :class="{ active: state.mode === 'surface' }" @click="state.mode = 'surface'">Surface S(u,v)</button>
        </div>

        <div class="control-group">
          <label>Weight ($w_i$): {{ state.weight.toFixed(2) }}</label>
          <input type="range" v-model.number="state.weight" min="0.1" max="5.0" step="0.1" />
          <p class="desc">Shows "Rational" property (pulls toward point)</p>
        </div>

        <div class="control-group" v-if="state.mode === 'curve'">
          <label>Knot ($u_i$): {{ state.knot.toFixed(2) }}</label>
          <input type="range" v-model.number="state.knot" min="0.1" max="0.9" step="0.05" />
          <p class="desc">Shows "Non-Uniform" property (parameter speed)</p>
        </div>

        <div class="control-group">
          <label>Parameter $u$: {{ state.u.toFixed(2) }}</label>
          <input type="range" v-model.number="state.u" min="0" max="1" step="0.01" />
        </div>

        <div class="control-group" v-if="state.mode === 'surface'">
          <label>Parameter $v$: {{ state.v.toFixed(2) }}</label>
          <input type="range" v-model.number="state.v" min="0" max="1" step="0.01" />
        </div>

        <div class="checkboxes">
          <label><input type="checkbox" v-model="state.showPoints" /> Points</label>
          <label><input type="checkbox" v-model="state.showPolygon" /> Polygon</label>
          <label v-if="state.mode === 'surface'"><input type="checkbox" v-model="state.showMesh" /> Mesh</label>
        </div>
      </div>

      <!-- Data Panel -->
      <div class="data-panel">
        <div class="data-section">
          <span class="label">Knot Vector:</span>
          <pre>{{ getKnotVector }}</pre>
        </div>
        <div class="data-section">
          <span class="label">STEP (Part 21) Preview:</span>
          <pre class="step-code">{{ getStepSnippet }}</pre>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.nurbs-viewer-wrapper {
  margin: 2rem 0;
  border: 1px solid var(--vp-c-divider);
  border-radius: 12px;
  overflow: hidden;
  background: #0f172a;
  font-family: var(--vp-font-family-base);
}

.viewer-container {
  display: grid;
  grid-template-columns: 1fr 300px;
  height: 500px;
}

@media (max-width: 850px) {
  .viewer-container {
    grid-template-columns: 1fr;
    grid-template-rows: 1fr auto;
    height: auto;
  }
  .canvas-container {
    height: 400px;
  }
}

.canvas-container {
  position: relative;
  min-height: 400px;
}

.overlay-controls {
  position: absolute;
  top: 1rem;
  left: 1rem;
  background: rgba(15, 23, 42, 0.8);
  backdrop-filter: blur(8px);
  padding: 1rem;
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: white;
  width: 240px;
  pointer-events: auto;
  z-index: 20;
}

.control-group {
  margin-bottom: 1rem;
}

.control-group label {
  display: block;
  font-size: 0.8rem;
  font-weight: 600;
  margin-bottom: 0.25rem;
  color: #94a3b8;
}

.control-group input[type="range"] {
  width: 100%;
}

.control-group .desc {
  font-size: 0.7rem;
  color: #64748b;
  margin: 0.25rem 0 0 0;
}

.tabs {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
}

.tabs button {
  flex: 1;
  background: #1e293b;
  border: 1px solid #334155;
  color: #94a3b8;
  padding: 0.4rem;
  font-size: 0.75rem;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
}

.tabs button.active {
  background: #3b82f6;
  color: white;
  border-color: #3b82f6;
}

.checkboxes {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  font-size: 0.75rem;
  color: #94a3b8;
}

.checkboxes label {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  cursor: pointer;
}

.data-panel {
  background: #1e293b;
  padding: 1.5rem;
  border-left: 1px solid #334155;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  overflow-y: auto;
}

.data-section {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.data-section .label {
  font-size: 0.75rem;
  font-weight: 700;
  color: #3b82f6;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.data-panel pre {
  margin: 0;
  padding: 0.75rem;
  background: #0f172a;
  border-radius: 6px;
  font-size: 0.7rem;
  color: #e2e8f0;
  white-space: pre-wrap;
  word-break: break-all;
  border: 1px solid #334155;
}

.step-code {
  color: #10b981 !important;
  font-family: 'Fira Code', monospace;
}
</style>
