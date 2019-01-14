<template>
  <q-page padding>
  <q-tabs class="shadow-1" animated swipeable inverted color="primary" glossy align="justify">

    <q-tab default slot="title" name="tab-2" label="Ground Floor" />
    <q-tab slot="title" name="tab-3" label="First Floor" />
    <q-tab slot="title" name="tab-4" label="Second Floor" />
    <q-tab slot="title" name="tab-5" label="Third Floor" />

    <q-tab-pane name="tab-2">Tab Two</q-tab-pane>
    <q-tab-pane name="tab-3">Tab Three</q-tab-pane>
    <q-tab-pane name="tab-4">Tab Four</q-tab-pane>
    <q-tab-pane name="tab-5">Tab Five</q-tab-pane>
  </q-tabs>
  </q-page>
</template>

<script>
export default {
  // name: 'PageName',
}
</script>

<style>
</style>
