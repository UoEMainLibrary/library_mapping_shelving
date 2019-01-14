<template>
  <q-page padding>
    <q-tabs class="shadow-1" animated swipeable inverted color="primary" glossy align="justify">
      <q-tab default slot='title' name='Hall' label='Hall' @select='loadData("/statics/floor_plans/newcollege0.json")'></q-tab>
      <q-tab slot='title' name='Stack_1' label='Stack 1' @select='loadData("/statics/floor_plans/newcollege1.json")'></q-tab>
      <q-tab slot='title' name='Stack_2' label='Stack 2' @select='loadData("/statics/floor_plans/newcollege2.json")'></q-tab>
      <q-tab-pane name='Hall' id='container' style = 'height:800px; width:800px;'></q-tab-pane>
      <q-tab-pane name='Stack_1' id='container' style = 'height:800px; width:800px;'></q-tab-pane>
      <q-tab-pane name='Stack_2' id='container' style = 'height:800px; width:800px;'></q-tab-pane>
    </q-tabs>
  </q-page>
</template>

<script>
import * as Three from 'three'
export default {
  methods: {
    degreesToRadians (degrees) {
      return degrees * Math.PI / 180
    },
    createElementObject (element, scaleFactor, offset) {
      let scaleX = element['scaleX']
      let scaleY = element['scaleY']
      let width = element['width'] * scaleX * scaleFactor
      let height = element['height'] * scaleY * scaleFactor
      let x = element['left']
      let y = element['top']
      // string representing shelf range
      let range = element['range_start_letters'] + ' ' + element['range_start'] + ' - ' + element['range_end_letters'] + ' ' + element['range_end']
      if (element['range_start'] === 'null') { range = '' }
      let degrees = element['angle']
      let geometry = new Three.BoxGeometry(width, height, 10)
      let color = new Three.Color('white')
      var meshMaterial = new Three.MeshLambertMaterial({color: color})
      let shelf = new Three.Mesh(geometry, meshMaterial)
      shelf.position.y = (0 + offset) - (y * scaleFactor)
      shelf.position.x = (0 - offset) + (x * scaleFactor)
      shelf.position.z = 3
      // convert angle to radians
      shelf.rotation.set(Math.PI / 1, 0, this.degreesToRadians(degrees))
      this.scene.add(shelf)
      // add text label
      let loader = new Three.FontLoader()
      loader.load('fonts/helvetiker_bold.typeface.json', function (font) {
        let xMid, text
        let color = 'darkred'
        let matDark = new Three.LineBasicMaterial({
          color: color,
          side: Three.DoubleSide
        })
        let matLite = new Three.MeshBasicMaterial({
          color: color,
          transparent: false,
          opacity: 0,
          side: Three.DoubleSide
        })
        let message = range
        let shapes = font.generateShapes(message, 0.35)
        let geometry = new Three.ShapeBufferGeometry(shapes)
        geometry.computeBoundingBox()
        xMid = 0.5 * (geometry.boundingBox.max.x - geometry.boundingBox.min.x)
        geometry.translate(xMid, 0, 0)
        // make shape ( N.B. edge view not visible )
        text = new Three.Mesh(geometry, matLite)
        text.position.x = shelf.position.x
        text.position.y = shelf.position.y
        text.position.z = shelf.position.z + 5.1
        text.rotation.set(Math.PI / 1, 0, this.degreesToRadians(degrees))
        text.rotation.y = (Math.PI / 2) * 2

        this.scene.add(text)
        // make line shape ( N.B. edge view remains visible )
        let holeShapes = []
        for (let i = 0; i < shapes.length; i++) {
          let shape = shapes[ i ]
          if (shape.holes && shape.holes.length > 0) {
            for (let j = 0; j < shape.holes.length; j++) {
              let hole = shape.holes[ j ]
              holeShapes.push(hole)
            }
          }
        }
        shapes.push.apply(shapes, holeShapes)
        let lineText = new Three.Object3D()
        for (let i = 0; i < shapes.length; i++) {
          let shape = shapes[ i ]
          let points = shape.getPoints()
          let geometry = new Three.BufferGeometry().setFromPoints(points)
          geometry.translate(xMid, 0, 0)
          let lineMesh = new Three.Line(geometry, matDark)
          lineText.add(lineMesh)
        }
        this.scene.add(lineText)
      }) // end load function
    },
    renderFloorPlan (data) {
      let container = document.getElementById('container')
      this.scene = new Three.Scene()
      this.scene.background = new Three.Color('lightgrey')
      // create camera
      this.camera = new Three.PerspectiveCamera(50, container.clientWidth / container.clientHeight, 1, 1000)
      this.camera.position.set(0, 0, 200)
      // add light
      let sunLight = new Three.DirectionalLight('rgb(255,255,255)', 1)
      sunLight.castShadow = false
      this.scene.add(sunLight)
      // renderer
      let renderer = new Three.WebGLRenderer({antialias: true})
      renderer.setPixelRatio(window.devicePixelRatio)
      renderer.setSize(window.clientWidth, window.clientHeight)
      container.appendChild(renderer.domElement)
      let geometry = new Three.BoxGeometry(0.2, 0.2, 0.2)
      let material = new Three.MeshNormalMaterial()
      this.mesh = new Three.Mesh(geometry, material)
      this.scene.add(this.mesh)
      this.renderer = new Three.WebGLRenderer({antialias: true})
      this.renderer.setSize(800, 800)
      container.appendChild(this.renderer.domElement)
      //  scale factor
      const scaleFactor = 0.05
      // offset
      const offset = 65
      for (let i in data['newcollege0']) {
        let element = JSON.parse(data['newcollege0'][i][0])
        if (element['name'] === 'Shelf') {
          console.log(element)
          this.createElementObject(element, scaleFactor, offset)
        }
      }
    },
    loadData (floor) {
      this.$axios.get(floor)
        .then((response) => {
          this.data = response.data
          this.renderFloorPlan(this.data)
        })
        .catch(() => {
          this.$q.notify({
            color: 'negative',
            position: 'top',
            message: 'Loading failed',
            icon: 'report_problem'
          })
        })
    }
  }
}

</script>

<style>
</style>
