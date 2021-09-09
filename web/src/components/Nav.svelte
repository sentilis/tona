<script>
	export let segment;
</script>

<nav class="navbar is-fixed-top">
	<div class="navbar-brand">
		<a class="navbar-item" href="/"> TONA </a>
		<div class="navbar-burger" data-target="tona-navbar-menu">
			<span />
			<span />
			<span />
		</div>
	</div>
	<div class="navbar-menu">
		<div class="navbar-end">
			<a
				rel="prefetch"
				aria-current={segment === "drive" ? "page" : undefined}
				class="navbar-item"
				href="drive"
			>
				Drive
			</a>
		</div>
	</div>
</nav>

<!--header class="pl-4 pr-4">
	<ul>
		<li><a aria-current="{segment === undefined ? 'page' : undefined}" href=".">home</a></li>
		<li><a aria-current="{segment === 'about' ? 'page' : undefined}" href="about">about</a></li>

		
		<li><a rel=prefetch aria-current="{segment === 'blog' ? 'page' : undefined}" href="blog">blog</a></li>
		<li><a rel=prefetch aria-current="{segment === 'drive' ? 'page' : undefined}" href="drive">Drive</a></li>
	</ul>
</header-->
