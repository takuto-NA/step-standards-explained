<script setup>
import { onMounted, ref, onBeforeUnmount } from 'vue'

const container = ref(null)

onMounted(async () => {
  // Use dynamic imports to avoid SSR issues
  const THREE = await import('three')
  const { NURBSSurface } = await import('three/addons/curves/NURBSSurface.js')
  const { ParametricGeometry } = await import('three/addons/geometries/ParametricGeometry.js')
  const { OrbitControls } = await import('three/addons/controls/OrbitControls.js')

  if (!container.value) return

  const width = container.value.clientWidth
  const height = 400

  const scene = new THREE.Scene()
  scene.background = new THREE.Color(0x1a1a1a)

  const camera = new THREE.PerspectiveCamera(75, width / height, 0.1, 1000)
  camera.position.set(5, 5, 5)

  const renderer = new THREE.WebGLRenderer({ antialias: true })
  renderer.setSize(width, height)
  renderer.setPixelRatio(window.devicePixelRatio)
  container.value.appendChild(renderer.domElement)

  const controls = new OrbitControls(camera, renderer.domElement)
  controls.enableDamping = true

  // NURBS Surface Data: 4x4 control points for a bicubic surface
  const nsControlPoints = [
    [
      new THREE.Vector4(-2, -2, 1, 1),
      new THREE.Vector4(-2, -1, -1, 1),
      new THREE.Vector4(-2, 1, -1, 1),
      new THREE.Vector4(-2, 2, 1, 1)
    ],
    [
      new THREE.Vector4(-1, -2, -1, 1),
      new THREE.Vector4(-1, -1, 2, 1),
      new THREE.Vector4(-1, 1, 2, 1),
      new THREE.Vector4(-1, 2, -1, 1)
    ],
    [
      new THREE.Vector4(1, -2, -1, 1),
      new THREE.Vector4(1, -1, 2, 1),
      new THREE.Vector4(1, 1, 2, 1),
      new THREE.Vector4(1, 2, -1, 1)
    ],
    [
      new THREE.Vector4(2, -2, 1, 1),
      new THREE.Vector4(2, -1, -1, 1),
      new THREE.Vector4(2, 1, -1, 1),
      new THREE.Vector4(2, 2, 1, 1)
    ]
  ]

  const degree1 = 3
  const degree2 = 3
  const knots1 = [0, 0, 0, 0, 1, 1, 1, 1]
  const knots2 = [0, 0, 0, 0, 1, 1, 1, 1]

  const nurbsSurface = new NURBSSurface(degree1, degree2, knots1, knots2, nsControlPoints)

  function getSurfacePoint(u, v, target) {
    return nurbsSurface.getPoint(u, v, target)
  }

  const geometry = new ParametricGeometry(getSurfacePoint, 24, 24)
  const material = new THREE.MeshPhongMaterial({
    color: 0x3498db,
    side: THREE.DoubleSide,
    transparent: true,
    opacity: 0.8,
    flatShading: false
  })
  const mesh = new THREE.Mesh(geometry, material)
  scene.add(mesh)

  // Wireframe
  const wireframeMaterial = new THREE.MeshBasicMaterial({ color: 0xffffff, wireframe: true, transparent: true, opacity: 0.2 })
  const wireframe = new THREE.Mesh(geometry, wireframeMaterial)
  scene.add(wireframe)

  // Control Points
  const pointsGeometry = new THREE.BufferGeometry()
  const pointsCoords = []
  for (let i = 0; i < nsControlPoints.length; i++) {
    for (let j = 0; j < nsControlPoints[i].length; j++) {
      pointsCoords.push(nsControlPoints[i][j].x, nsControlPoints[i][j].y, nsControlPoints[i][j].z)
    }
  }
  pointsGeometry.setAttribute('position', new THREE.Float32BufferAttribute(pointsCoords, 3))
  const pointsMaterial = new THREE.PointsMaterial({ color: 0xe74c3c, size: 0.1, sizeAttenuation: true })
  const points = new THREE.Points(pointsGeometry, pointsMaterial)
  scene.add(points)

  // Control Polygon (Grid Lines)
  const lineMaterial = new THREE.LineBasicMaterial({ color: 0x95a5a6, transparent: true, opacity: 0.4 })
  const lineGroup = new THREE.Group()
  
  // Rows
  for (let i = 0; i < nsControlPoints.length; i++) {
    const rowPoints = []
    for (let j = 0; j < nsControlPoints[i].length; j++) {
      rowPoints.push(new THREE.Vector3(nsControlPoints[i][j].x, nsControlPoints[i][j].y, nsControlPoints[i][j].z))
    }
    const rowGeom = new THREE.BufferGeometry().setFromPoints(rowPoints)
    lineGroup.add(new THREE.Line(rowGeom, lineMaterial))
  }
  // Columns
  for (let j = 0; j < nsControlPoints[0].length; j++) {
    const colPoints = []
    for (let i = 0; i < nsControlPoints.length; i++) {
      colPoints.push(new THREE.Vector3(nsControlPoints[i][j].x, nsControlPoints[i][j].y, nsControlPoints[i][j].z))
    }
    const colGeom = new THREE.BufferGeometry().setFromPoints(colPoints)
    lineGroup.add(new THREE.Line(colGeom, lineMaterial))
  }
  scene.add(lineGroup)

  // Lights
  const ambientLight = new THREE.AmbientLight(0xffffff, 0.6)
  scene.add(ambientLight)
  const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8)
  directionalLight.position.set(5, 10, 7.5)
  scene.add(directionalLight)

  let animationId;
  const animate = () => {
    animationId = requestAnimationFrame(animate)
    controls.update()
    renderer.render(scene, camera)
  }

  animate()

  const handleResize = () => {
    if (!container.value) return
    const newWidth = container.value.clientWidth
    camera.aspect = newWidth / height
    camera.updateProjectionMatrix()
    renderer.setSize(newWidth, height)
  }
  window.addEventListener('resize', handleResize)

  onBeforeUnmount(() => {
    window.removeEventListener('resize', handleResize)
    cancelAnimationFrame(animationId)
    
    renderer.dispose()
    geometry.dispose()
    material.dispose()
    wireframeMaterial.dispose()
    pointsGeometry.dispose()
    pointsMaterial.dispose()
    lineGroup.children.forEach(child => {
        child.geometry.dispose()
    })
    
    if (container.value && renderer.domElement) {
      container.value.removeChild(renderer.domElement)
    }
  })
})
</script>

<template>
  <div ref="container" class="nurbs-container">
    <div class="overlay">
      Bicubic NURBS Surface (4x4 Control Points)
    </div>
  </div>
</template>

<style scoped>
.nurbs-container {
  width: 100%;
  height: 400px;
  position: relative;
  border-radius: 8px;
  overflow: hidden;
  margin: 24px 0;
  border: 1px solid var(--vp-c-divider);
  background-color: #1a1a1a;
}

.overlay {
  position: absolute;
  top: 12px;
  left: 12px;
  background: rgba(0, 0, 0, 0.6);
  color: white;
  padding: 6px 10px;
  border-radius: 4px;
  font-size: 13px;
  font-family: var(--vp-font-family-base);
  pointer-events: none;
  z-index: 10;
  border: 1px solid rgba(255, 255, 255, 0.1);
}
</style>
