<template>
  <q-page padding>
    <q-tabs class='shadow-1' animated swipeable inverted color='primary' glossy align='justify'>
    <q-tab default slot="title" name="Murray1" label="First Floor" @select='loadData("/statics/floor_plans/murray1.json", "murray1")'/>
    <q-tab slot="title" name="Murray2" label="Second Floor" @select='loadData("/statics/floor_plans/murray2.json", "murray2")'/>
    <q-tab slot="title" name="Murray3" label="Third Floor" @select='loadData("/statics/floor_plans/murray3.json", "murray3")'/>
    <q-tab-pane name='Murray1'>
        <q-btn label="Publish" @click='publish()'/>
        <div id='container'></div>
    </q-tab-pane>
    <q-tab-pane name='Murray2'>
        <q-btn label="Publish" @click='publish()'/>
        <div id='container'></div>
    </q-tab-pane>
    <q-tab-pane name='Murray3'>
        <q-btn label="Publish" @click='publish()'/>
        <div id='container'></div>
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
        url: 'http://127.0.0.1:5000/update_ranges/', // url of end point
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
        .attr('height', 1000)
      for (let i in data[floorName]) {
        let element = JSON.parse(data[floorName][i][0])
        this.elements.push(element)
        // let degrees = element['angle']
        if (element['name'] === 'Shelf') {
          console.log(element)
          let y = element['left']
          let x = element['top'] - 1000
          let h = ''
          let w = ''
          if (floorName === 'murray1') {
            y = y - 600
          }
          let rotate = ''
          let scale = 0.5
          let shelfmark = ''
          if (element['range_start_digits'] != null) {
            shelfmark = element['range_start_letters'] + ' ' + element['range_start_digits'] + ' - ' + element['range_end_letters'] + ' ' + element['range_end_digits']
          } else { shelfmark = '' }
          console.log(shelfmark)
          w = element['width'] * element['scaleX']
          h = element['height'] * element['scaleY']
          rotate = 'rotate(0)'

          let rectangle = canvas.append('rect')
            .attr('x', x * scale)
            .attr('y', y * scale)
            .attr('width', w * scale)
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
            .attr('x', (x * scale) + 5)
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
