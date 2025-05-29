<script lang="ts">
	import '../app.css';
	let { children } = $props();
  </script>
  
  <!-- Full‐height flex container -->
  <div class="flex flex-col h-screen">
  
	<!-- HEADER: fixed at top of the flex container -->
	<header
	  class="p-4"
	  style="background-color: var(--skeleton-secondary); color: white;"
	>
	  <div class="flex justify-between items-center">
		<span class="text-xl font-bold">GLAM</span>
		<nav class="space-x-4">
		  <a href="https://mesnage-org.github.io/pgfinder"
			 target="_blank" rel="noopener"
			 class="hover:underline text-white">
			PGFinder
		  </a>
		  <a href="/glam/docs" class="hover:underline text-white">
			Documentation
		  </a>
		</nav>
	  </div>
	</header>
  
	<!-- MAIN: grows to fill available space and scrolls internally -->
	<main class="flex-1 overflow-auto p-6">
	  {@render children()}
	</main>
  
	<!-- FOOTER: fixed at bottom of the flex container -->
	<footer
	  class="p-4 text-center text-sm"
	  style="background-color: var(--skeleton-secondary); color: white;"
	>
	  Any issues or suggestions? Please get in touch!<br />
	  <a href="mailto:smesnage@sheffield.ac.uk"
		 class="font-semibold hover:underline text-white">
		smesnage@sheffield.ac.uk
	  </a>
	</footer>
  
  </div>
  