# GitHub Profile Summary & Statistics

This application retrieves a user's public GitHub data (e.g., basic profile info, repos, commits, etc.) and displays a summary along with a set of generated charts. The app offers:

- A user-friendly summary page with a snapshot of the user's GitHub profile.
- Additional stats such as:
  - **Repos per Language**
  - **Stars per Repo**
  - **Stars per Language**
  - **Public Commits per Repo**
  - **Commits per Language**
  - **Commits in the Last Year** (based on public commits)
- Interactive charts/graphs that can be embedded (via markdown) into your GitHub profile or other pages.

## Features

1. **Profile Info**  
   Displays the user's avatar, name, bio, company, email, location, and other public data from their GitHub profile.
2. **Statistics**  
   - Total public repositories, gists, followers, following count.
   - How long the user has been on GitHub.
3. **Clickable Charts**  
   - Each chart image is linked so you can open a full-size version.
   - MarkDown snippet included for each chart. Just **copy and paste** the snippet into your GitHub README or other Markdown files.
4. **Websites Deployed**  
   - A small list of the user’s deployed websites (if available in the data source).
5. **User Data & Repo Data Source**  
   - Each data source has a direct link (to GitHub API endpoints) so you can view the raw JSON behind the scenes.
6. **One-Day Server Cache**  
   - To avoid GitHub API saturation, the application caches data for one day. Graphs might be out of date until the cache refreshes next day.


## Embedding Charts in Your README

Each chart’s code block (Markdown snippet) looks like:

```
![]('https://github-summary.work.gd/graph?username=YOUR_USERNAME&graph_type=CHART_NAME')
```

- Replace `YOUR_USERNAME` with your actual GitHub username.
- Use the correct `CHART_NAME` as shown under each chart (e.g., `repos_per_language`, `stars_per_lang`, etc.).
- Copy/paste directly into your GitHub profile README or any other `.md` file.

## Caching Behavior

- The server caches data for 24 hours to minimize calls to GitHub’s API.
- If your GitHub profile changes or you gain more stars, you might not see the update until the following day.


## Acknowledgments
- Inspired by:
  - [Profile Summary for GitHub](https://profile-summary-for-github.com/search)
  - [GitHub Profile Summary Cards](https://github-profile-summary-cards.vercel.app/)

