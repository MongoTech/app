<template>
  <v-fade-transition mode="out-in">
    <router-view/>
  </v-fade-transition>
</template>

<script>
// Styles
import '@/styles/overrides.sass'
import {readIsLoggedIn} from '@/store/main/getters';
import {dispatchCheckLoggedIn} from '@/store/main/actions';

export default class App extends Vue {
  get loggedIn() {
    return readIsLoggedIn(this.$store);
  }

  async created() {
    await dispatchCheckLoggedIn(this.$store);
  }
}
</script>
