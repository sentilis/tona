<script>
    import { createEventDispatcher } from "svelte";
    import { DateToUTC, getBrowseTimeZone, URLJoin } from "../../utils";
    import { API_URL } from "../../constants";

    const dispatch = createEventDispatcher();

    export let group_by = "any";
    let dropdownDate = false;
    let dropdownExport = false;
    let filters = {};

    const applyFilter = (field, value) => {
        let params = {
            group_id: 0,
            group_by: group_by,
            skip: 0,
            limit: 50,
        };
        if (field == "start") {
            value = DateToUTC(new Date(value + "T00:00:00+00:00"));
            dropdownDate = false;
            filters["start__gte"] = value;
        } else if (field == "stop") {
            value = DateToUTC(new Date(value + "T23:59:59+00:00"));
            filters["stop__lte"] = value;
            dropdownDate = false;
        } else if (field == "export") {
            dropdownExport = false;
            params["export"] = value;
            params["limit"] = 0;
        }

        if (field == "undo") {
            filters = {};
        }

        if (Object.keys(filters).length) {
            params["filters"] = JSON.stringify(filters);
        }

        fetch(
            URLJoin(
                API_URL,
                `/api/v1/time-tracking/analyze?${new URLSearchParams(params)}`
            ),
            {
                method: "get",
                headers: {
                    Accept: "application/json",
                    "Content-Type": "application/json",
                    "tz": getBrowseTimeZone()
                },
            }
        )
            .then(async (res) => {
                if (res.status == 200) {
                    let body = await res.json();
                    dispatch("analyzeApplyFilters", {
                        entries: body["payload"],
                        meta: body["meta"]
                    });

                }
            })
            .catch((err) => {
                console.log(err);
            });
    };
</script>

<div class="field has-addons">
    <p class="control">
        <button class="button"> Filter by: </button>
    </p>

    <span class="control is-expanded">
        {#if group_by != "any"}
            <div class="dropdown">
                <div class="dropdown-trigger">
                    <button
                        class="button"
                        aria-haspopup="true"
                        aria-controls="dropdown-menu"
                    >
                        <span />
                        <span class="icon is-small">
                            <i class="fas fa-angle-down" aria-hidden="true" />
                        </span>
                    </button>
                </div>
                <div class="dropdown-menu" id="dropdown-menu" role="menu">
                    <div class="dropdown-content">
                        <a href="#" class="dropdown-item is-capitalized">
                            Dropdown item
                        </a>
                        <hr class="dropdown-divider" />
                        <a href="#" class="dropdown-item"> All </a>
                    </div>
                </div>
            </div>
        {/if}
        <div class="dropdown {dropdownDate ? 'is-active' : ''}">
            <div class="dropdown-trigger">
                <button
                    class="button"
                    aria-haspopup="true"
                    aria-controls="dropdown-menu"
                    on:click={() => (dropdownDate = !dropdownDate)}
                >
                    <span>Date</span>
                    <span class="icon is-small">
                        <i class="fas fa-angle-down" aria-hidden="true" />
                    </span>
                </button>
            </div>
            <div class="dropdown-menu" role="menu">
                <div class="dropdown-content">
                    <a class="dropdown-item">
                        <input
                            title="From"
                            class="input is-small"
                            data-date="start_date"
                            type="date"
                            on:change={(e) =>
                                applyFilter("start", e.target.value)}
                        />
                    </a>
                    <hr class="dropdown-divider" />
                    <a class="dropdown-item">
                        <input
                            title="To"
                            class="input is-small"
                            data-date="end_date"
                            type="date"
                            on:change={(e) =>
                                applyFilter("stop", e.target.value)}
                        />
                    </a>
                </div>
            </div>
        </div>
        <div class="dropdown {dropdownExport ? 'is-active' : ''}">
            <div class="dropdown-trigger">
                <button
                    class="button"
                    aria-haspopup="true"
                    aria-controls="dropdown-menu"
                    on:click={() => (dropdownExport = !dropdownExport)}
                >
                    <span>Export</span>
                    <span class="icon is-small">
                        <i class="fas fa-angle-down" aria-hidden="true" />
                    </span>
                </button>
            </div>
            <div class="dropdown-menu" id="dropdown-menu" role="menu">
                <div class="dropdown-content">
                    <a
                        class="dropdown-item"
                        on:click={() => applyFilter("export", "pdf")}
                    >
                        PDF
                    </a>
                    <hr class="dropdown-divider" />
                    <a
                        class="dropdown-item"
                        on:click={() => applyFilter("export", "csv")}
                    >
                        CSV
                    </a>
                </div>
            </div>
        </div>
    </span>
    <p class="control">
        <a
            class="button"
            title="Undo filters"
            on:click={() => applyFilter("undo", "")}
        >
            <span class="icon">
                <i class="fas fa-undo" aria-hidden="true" />
            </span>
        </a>
    </p>
</div>
