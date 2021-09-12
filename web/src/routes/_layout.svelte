<svelte:head>
  <style src="../../node_modules/bulma/css/bulma.css"></style>
  <!--link rel="stylesheet" src="../../node_modules/@fortawesome/fontawesome-free/css/all.min.css"-->
  <link rel="stylesheet" href="https://bulma.io/vendor/fontawesome-free-5.15.2-web/css/all.min.css">

</svelte:head>

<script>

	import Nav from '../components/Nav.svelte';

	export let segment;
</script>


<Nav {segment}/>

<main class="ml-5 mr-5 mt-4 pt-6">
	<slot></slot>
</main>