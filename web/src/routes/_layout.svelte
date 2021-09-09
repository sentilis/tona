<svelte:head>
  <style src="../../node_modules/bulma/css/bulma.css"></style>
  <link rel="stylesheet" href="../../@fontawesome/fontawesome-free/css/all.min.css">
</svelte:head>

<script>

	import Nav from '../components/Nav.svelte';

	export let segment;
</script>


<Nav {segment}/>

<main class="ml-5 mr-5 mt-4 pt-6">
	<slot></slot>
</main>