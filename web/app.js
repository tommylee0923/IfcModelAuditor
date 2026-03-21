// ============================================================
// #region STATE
// ============================================================
const state = {
    runs: [],           // all audit runs fetched from /runs
    issues: [],         // issues for the currently selected run
    activeRunId: null,  // which run the user has clicked into
};
// #endregion

// ============================================================
// #region DOM REFERENCES
// ============================================================

const runsView    = document.getElementById("runs-view");
const detailView  = document.getElementById("detail-view");
const runsList    = document.getElementById("runs-list");
const runHeader   = document.getElementById("run-header");
const issuesList  = document.getElementById("issues-list");
const backBtn     = document.getElementById("back-btn");
const classFilter = document.getElementById("class-filter");
// #endregion

// ============================================================
//#region API CALLS
// ============================================================

async function fetchRuns() {
    try {
        const response = await fetch("/runs");
        if (!response.ok) {
            throw new Error(`Server returned ${response.status}`);
        }
        return await response.json();
    } catch (err) {
        showError(runsList, `Could not load audit runs: ${err.message}`);
        return [];
    }
}

async function fetchIssues(runId) {
    try {
        const response = await fetch(`/runs/${runId}/issues`);
        if (!response.ok) {
            throw new Error(`Server returned ${response.status}`);
        }
        return await response.json();
    } catch (err) {
        showError(issuesList, `Could not load issues: ${err.message}`);
        return [];
    }
}
// #endregion


// ============================================================
//#region RENDER FUNCTIONS
// ============================================================

function renderRuns(runs) {
    if (runs.length === 0) {
        showEmpty(runsList, "No audit runs found. Run an audit first.");
        return;
    }

    const html = `
        <div class="runs-grid">
            ${runs.map(run => `
                <div class="run-card" data-run-id="${run.id}">
                    <div class="run-card-left">
                        <div class="run-filename">${escapeHtml(run.source_file)}</div>
                        <div class="run-timestamp">${run.run_timestamp}</div>
                    </div>
                    <div class="run-card-right">
                        <span class="badge badge-neutral">${run.total_elements} elements</span>
                        <span class="badge badge-issue">${run.total_issues} issues</span>
                    </div>
                </div>
            `).join("")}
        </div>
    `;

    runsList.innerHTML = html;

    runsList.addEventListener("click", (event) => {
        const card = event.target.closest(".run-card");
        if (!card) return;
        const runId = parseInt(card.dataset.runId, 10);
        openRun(runId);
    });
}

function renderRunHeader(run) {
    runHeader.innerHTML = `
        <div>
            <div class="run-header-title">${escapeHtml(run.source_file)}</div>
            <div class="run-header-meta">Run ID: ${run.id} &nbsp;·&nbsp; ${run.run_timestamp}</div>
        </div>
        <div class="run-header-stats">
            <span class="badge badge-neutral">${run.total_elements} elements</span>
            <span class="badge badge-issue">${run.total_issues} issues</span>
        </div>
    `;
}

function renderIssues(issues) {
    if (issues.length === 0) {
        showEmpty(issuesList, "No issues found for this run.");
        return;
    }

    const html = `
        <table class="issues-table">
            <thead>
                <tr>
                    <th>Code</th>
                    <th>Message</th>
                    <th>IFC Class</th>
                    <th>GlobalID</th>
                </tr>
            </thead>
            <tbody>
                ${issues.map(issue => `
                    <tr>
                        <td><span class="issue-code">${escapeHtml(issue.issue_code)}</span></td>
                        <td>
                            <div class="issue-message">${escapeHtml(issue.message)}</div>
                            ${issue.element_name
                                ? `<div class="issue-meta">${escapeHtml(issue.element_name)}</div>`
                                : ""}
                        </td>
                        <td>${escapeHtml(issue.ifc_class || "Unknown")}</td>
                        <td><span class="global-id">${escapeHtml(issue.global_id)}</span></td>
                    </tr>
                `).join("")}
            </tbody>
        </table>
    `;

    issuesList.innerHTML = html;
}

function populateClassFilter(issues) {
    const classes = [...new Set(issues.map(i => i.ifc_class || "Unknown"))].sort();

    classFilter.innerHTML = `<option value="">All Classes</option>`;

    classes.forEach(cls => {
        const option = document.createElement("option");
        option.value = cls;
        option.textContent = cls;
        classFilter.appendChild(option);
    });
}
// #endregion

// ============================================================
//#region NAVIGATION
// ============================================================

async function openRun(runId) {
    state.activeRunId = runId;

    const run = state.runs.find(r => r.id === runId);

    const issues = await fetchIssues(runId);
    state.issues = issues;

    renderRunHeader(run);
    renderIssues(issues);
    populateClassFilter(issues);

    runsView.classList.add("hidden");
    detailView.classList.remove("hidden");
}

function goBack() {
    state.activeRunId = null;
    state.issues = [];

    classFilter.value = "";

    detailView.classList.add("hidden");
    runsView.classList.remove("hidden");
}
//#endregion

// ============================================================
//#region FILTERING
// ============================================================

function applyFilter() {
    const selected = classFilter.value;

    const filtered = selected
        ? state.issues.filter(i => (i.ifc_class || "Unknown") === selected)
        : state.issues;

    renderIssues(filtered);
}
// #endregion

// ============================================================
//#region HELPERS
// ============================================================

function showEmpty(container, message) {
    container.innerHTML = `<div class="state-message">${message}</div>`;
}

function showError(container, message) {
    container.innerHTML = `<div class="state-message error">${message}</div>`;
}

function escapeHtml(str) {
    if (str == null) return "";
    return String(str)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;");
}
// #endregion

// ============================================================
//#region EVENT LISTENERS
// ============================================================

backBtn.addEventListener("click", goBack);
classFilter.addEventListener("change", applyFilter);
// #endregion

// ============================================================
//#region INIT
// ============================================================

(async () => {
    const runs = await fetchRuns();
    state.runs = runs;
    renderRuns(runs);
})();