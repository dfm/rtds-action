const core = require("@actions/core");
const github = require("@actions/github");
const fetch = require("node-fetch");

try {
  const webhookId = core.getInput("webhook_id", { required: true });
  const webhookToken = core.getInput("webhook_token", { required: true });

  // Extract the branch name from the ref
  const ref = github.context.payload.ref;
  const branchname = ref.split("/").slice(2).join("/");

  // Format the URL and parameters
  const url = `https://readthedocs.org/api/v2/webhook/${webhookId}/`;
  const params = new URLSearchParams();
  params.append("branches", branchname);
  params.append("token", webhookToken);

  // Execute the request
  (async () => {
    try {
      const response = await fetch(url, {
        method: "POST",
        body: params,
      });
      const json = await response.json();
      console.log(json);
    } catch (error) {
      core.setFailed(error.message);
    }
  })();
} catch (error) {
  core.setFailed(error.message);
}
