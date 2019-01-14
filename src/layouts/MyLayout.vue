<template>
  <q-layout view="lHh Lpr lFf">
    <q-layout-header>
      <q-toolbar
        color="primary"
        :glossy="$q.theme === 'mat'"
        :inverted="$q.theme === 'ios'"
      >
        <q-btn
          flat
          dense
          round
          @click="leftDrawerOpen = !leftDrawerOpen"
          aria-label="Menu"
        >
          <q-icon name="menu" />
        </q-btn>
        <q-toolbar-title>
          Library Shelving
        </q-toolbar-title>
      </q-toolbar>
    </q-layout-header>

    <q-layout-drawer
      v-model="leftDrawerOpen"
      :content-class="$q.theme === 'mat' ? 'bg-grey-2' : null"
    >
    <img alt="Quasar logo" width="250" src="~assets/edinburgh_university_logo.png">
      <q-list
        no-border
        link
        inset-delimiter
      >
        <q-list-header>Select Library</q-list-header>
        <q-item to='/main/'>
          <q-item-side icon="school" />
          <q-item-main label="Main Library" sublabel="George Square" />
        </q-item>
        <q-item to='/new_college/'>
          <q-item-side icon="school" />
          <q-item-main label="New College Library" sublabel="The Mound" />
        </q-item>
        <q-item to='/murray/'>
          <q-item-side icon="school" />
          <q-item-main label="Murray Library" sublabel="King's Buildings" />
        </q-item>
      </q-list>
    </q-layout-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
import { openURL } from 'quasar'

export default {
  name: 'MyLayout',
  data () {
    return {
      leftDrawerOpen: this.$q.platform.is.desktop
    }
  },
  methods: {
    openURL
  }
}
</script>

<style>
</style>
