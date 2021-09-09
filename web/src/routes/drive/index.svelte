<script context="module">
    export function preload() {
        runLocalSync(this);
        return getContentFolder(this).then((folder) => {
            return { folder };
        });
    }
</script>

<script>
    import Workspace2 from "../../components/Workspace2.svelte";
    import ModalFile from "./ModalFile.svelte";
    import { getContentFolder, runLocalSync, routeBreadcrumbs } from "./index";

    export let folder;
    let breadcrumbs = [{ id: 0, name: "Root" }];

    async function folderClicked(id, name) {
        return getContentFolder(id).then((f) => {
            folder = f;
            breadcrumbs = routeBreadcrumbs(breadcrumbs, id, name);
        });
    }

    let propsModal = {};
    let fileClicked = (file) => {
        propsModal = { file: file, isActive: true };
    };
</script>

<Workspace2>
    <aside slot="column-one" class="menu">
        <p class="menu-label">My Drive</p>
        <ul class="menu-list">
            {#each folder.folders as folder}
                <li>
                    <a on:click={folderClicked(folder.id, folder.name)}>
                        <span class="icon-text">
                            <span class="icon">
                                <i class="fas fa-folder" />
                            </span>
                            <span>{folder.name}</span>
                        </span>
                    </a>
                </li>
            {/each}
        </ul>
    </aside>
    <div slot="column-two">
        <nav class="breadcrumb" aria-label="breadcrumbs">
            <ul>
                {#each breadcrumbs as breadcrumb}
                    <li>
                        <a
                            on:click={folderClicked(
                                breadcrumb.id,
                                breadcrumb.name
                            )}
                        >
                            {breadcrumb.name}
                        </a>
                    </li>
                {/each}
            </ul>
        </nav>

        {#if folder.folders.length}
            <div class="columns is-mobile">Folders</div>
        {/if}
        <div id="drive-folders" class="columns is-multiline is-mobile">
            {#each folder.folders as folder}
                <div
                    class="column is-clickable card"
                    on:click={folderClicked(folder.id, folder.name)}
                >
                    <span class="icon-text">
                        <span class="icon">
                            <i class="fas fa-folder" />
                        </span>
                        <span>{folder.name}</span>
                    </span>
                </div>
            {/each}
        </div>
        {#if folder.files.length}
            <div class="columns is-mobile">Files</div>
        {/if}

        <div id="drive-files" class="columns is-mobile">
            {#each folder.files as file}
                <div
                    class="column is-clickable card"
                    on:click={fileClicked(file)}
                >
                    <span class="icon-text">
                        <span class="icon">
                            <i class="fas fa-file" />
                        </span>
                    </span>
                    {file.name}
                </div>
            {/each}
            <svelte:component this={ModalFile} {...propsModal} />
        </div>
    </div>
</Workspace2>
