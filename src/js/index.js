const core = require("@actions/core");
const github = require("@actions/github");
const fetch = require("node-fetch");

try {
  const webhookUrl = core.getInput("webhook_url", { required: true });
  const webhookToken = core.getInput("webhook_token", { required: true });

  // Extract the branch name from the ref
  const ref = github.context.payload.ref;
  const branchname = ref.split("/").slice(2).join("/");

  // Format the request parameters
  const params = new URLSearchParams();
  params.append("branches", branchname);
  params.append("token", webhookToken);

  // Execute the request
  (async () => {
    try {
      const response = await fetch(webhookUrl, {
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
