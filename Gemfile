source "https://rubygems.org"

# Matches the GitHub Pages build environment so local preview == live.
gem "github-pages", group: :jekyll_plugins

# Ruby 3.0+ no longer ships webrick; Jekyll's local server needs it.
gem "webrick"

# Reliable file-change watching on Windows (otherwise --watch falls back to
# slow/flaky polling and may serve stale pages).
gem "wdm", ">= 0.1.0", platforms: [:mingw, :x64_mingw, :mswin]
