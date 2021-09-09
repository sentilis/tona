<script>
    import { API_URL } from "../../constants";
    import { URLJoin, Clipboard } from "../../utils";

    export let file = null;
    export let isActive = false;
</script>

<div class="modal {isActive ? 'is-active' : ''}">
    <div class="modal-background" />
    <div class="modal-card">
        <header class="modal-card-head">
            <p class="modal-card-title">{file?.name}</p>

            <div class="control is-inline is-pulled-right">
                <a title="Copy Path" on:click={() => Clipboard(file?.file)}>
                    <span class="icon">
                        <i class="fas fa-link" />
                    </span>
                </a>
                <a
                    title="Download"
                    href={URLJoin(
                        API_URL,
                        "/api/v1/drive/files/" + file?.id + "/download"
                    )}
                    target="_black"
                >
                    <span class="icon">
                        <i class="fas fa-download" />
                    </span>
                </a>
                <a
                    title="Share Link"
                    on:click={Clipboard(
                        URLJoin(
                            API_URL,
                            "/api/v1/drive/files/" + file?.id + "/preview"
                        )
                    )}
                >
                    <span class="icon">
                        <i class="fas fa-share-alt" />
                    </span>
                </a>

                <button
                    class="delete"
                    aria-label="close"
                    on:click={() => (isActive = false)}
                />
            </div>
        </header>
        <section class="modal-card-body">
            {#if file?.mimetype.match(/^image/)}
                <figure class="image">
                    <img
                        src={URLJoin(
                            API_URL,
                            "/api/v1/drive/files/" + file.id + "/preview"
                        )}
                    />
                </figure>
            {:else if file?.mimetype.match(/^video/)}
                <video controls>
                    <source
                        src={URLJoin(
                            API_URL,
                            "/api/v1/drive/files/" + file?.id + "/preview"
                        )}
                        type={file?.mimetype}
                    />
                </video>
            {:else if file?.mimetype.match(/^audio/)}
                <audio controls>
                    <source
                        src={URLJoin(
                            API_URL,
                            "/api/v1/drive/files/" + file?.id + "/preview"
                        )}
                        type={file.mimetype}
                    />
                </audio>
            {:else if file?.mimetype.match(/^text/)}
                <figure class="image is-16by9">
                    <iframe
                        class="has-ratio"
                        src={URLJoin(
                            API_URL,
                            "/api/v1/drive/files/" + file?.id + "/preview"
                        )}
                        allowfullscreen
                    />
                </figure>
            {:else}
                {file?.mimetype}
            {/if}
        </section>
        <!--footer class="modal-card-foot">
            <button class="button is-success">Download</button>
            <button class="button is-success">Copy Path</button>
        </footer-->
    </div>
</div>
