<script context="module">
    export function preload() {
        return getLastEntries(this).then((lastEntries) => {
            return { lastEntries };
        });
    }
</script>

<script>
    import Workspace3 from "../../components/Workspace3.svelte";
    import Timer from "./Timer.svelte";
    import Filter from "./Filter.svelte";

    import {
        getLastEntries,
        formatDuration,
        entryEdit,
        entryDelete,
        downloadExportTo,
    } from "./index";
    import moment from "moment-timezone";

    import { getBrowseTimeZone, getHTML5DateTime } from "../../utils";

    export let lastEntries;
    let entrySelected;
    let menu = "";

    let entrySelectedMenuActive;
    const entrySelectedMenu = () => {
        entrySelectedMenuActive = !entrySelectedMenuActive;
    };

    const entryStartStopOnBlur = (field, value) => {
        function duration() {
            let diff =
                new Date(entrySelected.stop).getTime() -
                new Date(entrySelected.start).getTime();
            entrySelected.duration = Math.floor(diff / 1000);
        }
        if (field == "start") {
            entrySelected.start = value;
            duration();
            entryEdit("start", entrySelected);
        } else if (field == "stop") {
            entrySelected.stop = value;
            duration();
            entryEdit("start", entrySelected);
        }
    };

    const menuOnClick = (val) => {
        console.log(val);
        if (val == "analyze-any") {
            menu = val;
        } else {
            menu = "";
        }
    };

    const getAnalyzeEntries = (event) => {
        let metaHas = false;
        let fname = "";
        if (event.detail["meta"] !== null) {
            (event.detail["meta"] || []).forEach((row) => {
                if (row["slug"] === "export-to") {
                    metaHas = true;
                    fname = row["value"];
                }
            });
        }
        if (event.detail["entries"] !== null && !metaHas) {
            lastEntries = event.detail["entries"];
        }
        if (metaHas) {
            downloadExportTo(fname)
        }
    };
</script>

<Workspace3>
    <aside class="menu" slot="column-one">
        <p class="menu-label">Track</p>
        <ul class="menu-list">
            <li><a on:click={() => menuOnClick("timer")}>Timer</a></li>
        </ul>
        <p class="menu-label">Analyze</p>
        <ul class="menu-list">
            <li><a on:click={() => menuOnClick("analyze-any")}>Any</a></li>
            <!--li><a on:click={() => (menu = "analyze-project")}>Project</a></li>
            <li>
                <a on:click={() => (menu = "analyze-objective")}>Objective</a>
            </li>
            <li><a on:click={() => (menu = "analyze-habit")}>Habit</a></li-->
        </ul>
    </aside>
    <div class="column" slot="column-two">
        <div class="columns">
            <div class="column">
                {#if menu == ""}
                    <Timer />
                {:else}
                    <Filter on:analyzeApplyFilters={getAnalyzeEntries} />
                {/if}
            </div>
        </div>
        <table class="table is-hoverable is-narrow is-fullwidth">
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Duration</th>
                </tr>
            </thead>
            <!--tfoot>
              <tr>
                <th><abbr title="Position">Pos</abbr></th>                
              </tr>
            </tfoot -->
            <tbody>
                {#each lastEntries as lastEntry}
                    <tr
                        class="is-clickable"
                        on:click={() => (entrySelected = lastEntry)}
                    >
                        <td
                            >{lastEntry["name"]} <br />
                            <span class="content is-small">
                                {moment(lastEntry["start"])
                                    .tz(getBrowseTimeZone())
                                    .calendar()}
                            </span>
                            -
                            <span class="content is-small">
                                {moment(lastEntry["stop"])
                                    .tz(getBrowseTimeZone())
                                    .calendar()}
                            </span>
                        </td>
                        <td>{formatDuration(lastEntry["duration"])}</td>
                    </tr>
                {/each}
            </tbody>
        </table>
    </div>

    <div class="columns" slot="column-three">
        {#if entrySelected}
            <div class="column">
                <div class="control is-inline is-pulled-right">
                    <div
                        class="dropdown is-right {entrySelectedMenuActive
                            ? 'is-active'
                            : ''}"
                    >
                        <div class="dropdown-trigger">
                            <button
                                class="button is-small"
                                aria-haspopup="true"
                                aria-controls="time-entry-menu"
                                on:click={entrySelectedMenu}
                            >
                                <span class="icon is-small">
                                    <i class="fas fa-bars" aria-hidden="true" />
                                </span>
                            </button>
                        </div>
                        <div
                            class="dropdown-menu"
                            id="time-entry-menu"
                            role="menu"
                        >
                            <div class="dropdown-content">
                                <a
                                    on:click={() => {
                                        entrySelectedMenu();
                                        entryDelete(entrySelected);
                                    }}
                                    class="dropdown-item"
                                >
                                    Delete
                                </a>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="field">
                    <label class="label is-small">Duration</label>

                    <div class="control">
                        <input
                            id="time-entry-start-stop"
                            class="input is-small is-static"
                            readonly
                            type="text"
                            value={formatDuration(entrySelected["duration"])}
                        />
                    </div>
                </div>
                <div class="field">
                    <label class="label is-small">Name</label>
                    <div class="control">
                        <input
                            on:blur={entryEdit("name", entrySelected)}
                            class="input is-small"
                            type="text"
                            bind:value={entrySelected.name}
                        />
                    </div>
                </div>

                <div class="field">
                    <label class="label is-small">Start</label>
                    <div class="control">
                        <input
                            on:blur={(e) =>
                                entryStartStopOnBlur("start", e?.target?.value)}
                            class="input is-small"
                            type="datetime-local"
                            step="1"
                            value={getHTML5DateTime(entrySelected.start)}
                        />
                    </div>
                </div>

                <div class="field">
                    <label class="label is-small">Stop</label>
                    <div class="control">
                        <input
                            on:blur={(e) =>
                                entryStartStopOnBlur("stop", e?.target?.value)}
                            class="input is-small"
                            type="datetime-local"
                            step="1"
                            value={getHTML5DateTime(entrySelected["stop"])}
                        />
                    </div>
                </div>
                {#if entrySelected["res_id"] && entrySelected["res_model"]}
                    <div class="field">
                        <label class="label is-small">Resource ID</label>
                        <div class="control">
                            <input
                                class="input is-small"
                                type="number"
                                bind:value={entrySelected.res_id}
                            />
                        </div>
                    </div>

                    <div class="field">
                        <label class="label is-small">Resource Name</label>
                        <div class="control">
                            <input
                                class="input is-small"
                                type="text"
                                bind:value={entrySelected.res_model}
                            />
                        </div>
                    </div>
                {/if}
            </div>
        {/if}
    </div>
</Workspace3>
