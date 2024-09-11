const express = require("express");
const path = require("path");
const app = express();

// Serve static files from the "public" directory
app.use(express.static(path.join(__dirname, "public")));

// Home route that serves the HTML page
app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "index.html"));
});

// Start the server
const port = 3001;
app.listen(port, () => {
  console.log(`Node server is running on http://localhost:${port}`);
});
