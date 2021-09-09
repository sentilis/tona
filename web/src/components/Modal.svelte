<script>
    export let title = "";
    export let isActive=false;
</script>

<div class="modal {isActive ? 'is-active': '' }">
    <div class="modal-background" />
    <div class="modal-card">
        <header class="modal-card-head">
            <p class="modal-card-title">{title}</p>
            <button
                class="delete is-large"
                aria-label="close"
                on:click={() => (isActive = false)}
            />
        </header>
        <section class="modal-card-body">
            <slot name="body"></slot>
        </section>
        <footer class="modal-card-foot">
            <slot name="foot"></slot>
        </footer>
    </div>
</div>
