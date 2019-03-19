<template>
  <q-page padding>
    <q-tabs class='shadow-1' animated swipeable inverted color='primary' glossy align='justify'>
    <q-tab default slot="title" name="groundFloor" label="Ground Floor" @select='loadData("/statics/floor_plans/main1.json", "main1")'/>
    <q-tab slot="title" name="secondFloor" label="Second Floor" @select='loadData("/statics/floor_plans/main3.json", "main3")'/>
    <q-tab slot="title" name="thirdFloor" label="Third Floor" @select='loadData("/statics/floor_plans/main4.json", "main4")'/>
    <q-tab slot="title" name="fourthFloor" label="Fourth Floor" @select='loadData("/statics/floor_plans/main5.json", "main5")'/>
    <q-tab-pane name='groundFloor'>
        <q-btn label="Publish" @click='publish()'/>
        <div id='container' style='overflow:scroll; height: 700px; width: 1100px;' ></div>
    </q-tab-pane>
    <q-tab-pane name='secondFloor' >
        <q-btn label="Publish" @click='publish()'/>
        <div id='container' style='overflow:scroll; height: 700px; width: 1100px;' ></div>
    </q-tab-pane>
    <q-tab-pane name='thirdFloor'>
        <q-btn label="Publish" @click='publish()'/>
        <div id='container' style='overflow:scroll; height: 700px; width: 1100px;' ></div>
      </q-tab-pane>
      <q-tab-pane name='fourthFloor'>
          <q-btn label="Publish" @click='publish()'/>
          <div id='container' style='overflow:scroll; height: 700px; width: 1100px;' ></div>
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
        .attr('width', 1500)
        .attr('height', 4000)
      for (let i in data[floorName]) {
        let element = JSON.parse(data[floorName][i][0])
        this.elements.push(element)
        // let degrees = element['angle']
        if (element['name'] === 'Shelf') {
          console.log(element)
          let y = element['left'] - 700
          let x = element['top'] - 200
          let w = element['width']
          let h = element['height']
          // x,y modifications for each tab
          if (floorName === 'main3') {
            x = x / 2.3
            y = (y * 1.4) + 600
            w = w * 1.5
          }
          if (floorName === 'main4') {
            x = x / 2.3
            y = (y * 1.4) - 1750
            w = w * 1.5
          }
          if (floorName === 'main5') {
            x = x / 2.3
            y = (y * 1.4) + 600
            w = w * 1.5
          }
          let rotate = ''
          let scale = 1
          let shelfmark = ''
          if (element['range_start_digits'] != null) {
            shelfmark = element['range_start_letters'] + ' ' + element['range_start_digits'] + ' - ' + element['range_end_letters'] + ' ' + element['range_end_digits']
          } else { shelfmark = '' }
          console.log(shelfmark)

          rotate = 'rotate(0)'

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
  height: 2000px;
  width: 6000px;
}
</style>
