<template>
  <q-page padding>
    <q-tabs class='shadow-1' animated swipeable inverted color='primary' glossy align='justify'>
      <q-tab default slot='title' name='Hall' label='Hall' @select='loadData("/statics/floor_plans/newcollege2.json", "newcollege2")'></q-tab>
      <q-tab slot='title' name='Stack_1' label='Stack 1' @select='loadData("/statics/floor_plans/newcollege1.json", "newcollege1")'></q-tab>
      <q-tab slot='title' name='Stack_2' label='Stack 2' @select='loadData("/statics/floor_plans/newcollege0.json", "newcollege0")'></q-tab>
      <q-tab-pane name='Hall'>
        <q-btn label="Publish" @click='publish()'/>
        <div id='container' style='overflow:scroll; height: 700px; width: 1100px;'></div>
      </q-tab-pane>
      <q-tab-pane name='Stack_1'>
        <q-btn label="Publish" @click='publish()'/>
        <div id='container' style='overflow:scroll; height: 700px; width: 1100px;'></div>
      </q-tab-pane>
      <q-tab-pane name='Stack_2'>
        <q-btn label="Publish" @click='publish()'/>
        <div id='container' style='overflow:scroll; height: 700px; width: 1100px;'></div>
      </q-tab-pane>
    </q-tabs>
  </q-page>
</template>

<script>
import * as d3 from 'd3'

export default {
  data () {
    return {
      elements: []
    }
  },
  methods: {
    publish () {
      // push these to remote api, possibly using axios
      this.$axios({
        method: 'post',
        url: '', // url of end point
        data: {elements: this.elements}
      })
        .then(function (response) {
          console.log(response)
        })
        .catch(function (error) {
          console.log(error)
        })
    },
    renderFloorPlan (data, floorName) {
      let canvas = d3.select('#container').append('svg')
        .attr('width', 3000)
        .attr('height', 1500)
      for (let i in data[floorName]) {
        let element = JSON.parse(data[floorName][i][0])
        this.elements.push(element)
        let degrees = element['angle']
        if (element['name'] === 'Shelf') {
          let x = element['left'] * 2 // * element['scaleX']
          let y = element['top'] * 2 // * element['scaleY']
          let h = ''
          let w = ''
          let rotate = ''
          let scale = 1
          let shelfmark = ''
          if (element['range_start_digits'] != null) {
            shelfmark = element['range_start_letters'] + ' ' + element['range_start_digits'] + ' - ' + element['range_end_letters'] + ' ' + element['range_end_digits']
          } else { shelfmark = '' }
          console.log(shelfmark)
          if (degrees < 1) {
            w = element['width']
            h = element['height']
            rotate = 'rotate(0)'
          } else {
            h = element['width']
            w = element['height']
            rotate = 'rotate(90)'
          }
          let rectangle = canvas.append('rect')
            .attr('x', x * scale)
            .attr('y', y * scale)
            .attr('width', w * 0.5)
            .attr('height', h * scale)
            .style('fill', 'white')
            .style('opacity', '1')
            .style('stroke', '#031b3d')
            .style('stroke-width', '2')
            .on('click', function () {
              console.log(element['id'])
              console.log(element['range_start_letters'], element['range_start_digits'], element['range_end_letters'], element['range_end_digits'])
              element['range_start_letters'] = prompt('Please enter range start letters:', element['range_start_letters'])
              element['range_start_digits'] = prompt('Please enter range start digits:', element['range_start_digits'])
              element['range_end_letters'] = prompt('Please enter range end letters:', element['range_end_letters'])
              element['range_end_digits'] = prompt('Please enter range end digits:', element['range_end_digits'])
              shelfmark = element['range_start_letters'] + ' ' + element['range_start_digits'] + ' - ' + element['range_end_letters'] + ' ' + element['range_end_digits']
              text.text(shelfmark)
              console.log(text)
            })
          console.log(rectangle)
          // label rectangle
          let text = canvas.append('text')
            // .attr('transform', rotate)
            .attr('x', (x * scale) + 10)
            .attr('y', (y * scale) + 12)
            .text(shelfmark)
            .attr('font-family', 'sans-serif')
            .attr('font-size', '12px')
            .attr('fill', 'darkred')
            .style('font-weight', 'bold')
            .on('click', function () {
              console.log(element['id'])
              console.log(element['range_start_letters'], element['range_start_digits'], element['range_end_letters'], element['range_end_digits'])
              element['range_start_letters'] = prompt('Please enter range start letters:', element['range_start_letters'])
              element['range_start_digits'] = prompt('Please enter range start digits:', element['range_start_digits'])
              element['range_end_letters'] = prompt('Please enter range end letters:', element['range_end_letters'])
              element['range_end_digits'] = prompt('Please enter range end digits:', element['range_end_digits'])
              shelfmark = element['range_start_letters'] + ' ' + element['range_start_digits'] + ' - ' + element['range_end_letters'] + ' ' + element['range_end_digits']
              text.text(shelfmark)
              console.log(text)
            })
          console.log(rotate)
          console.log(text)
        }
      }
    },
    loadData (floor, floorName, library) {
      this.$axios
        .get(floor)
        .then(response => {
          this.floorName = floorName
          this.renderFloorPlan(response.data, floorName, library)
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
#container {
  height: auto;
  width: 800px;
}
</style>
