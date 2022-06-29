<template>
  <v-fade-transition mode="out-in">
    <router-view/>
  </v-fade-transition>
</template>

<script>

import './styles/overrides.sass'
import {readIsLoggedIn} from './store/main/getters.ts';
import {dispatchCheckLoggedIn} from './store/main/actions.ts';

export default class App extends Vue {
  get loggedIn() {
    return readIsLoggedIn(this.$store);
  }

  async created() {
    await dispatchCheckLoggedIn(this.$store);
  }
}
</script>
