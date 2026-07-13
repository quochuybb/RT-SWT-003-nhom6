---
hide:
  - navigation
---

# Release Notes

## Latest Changes

### Translations

* 🌐 Fix broken Markdown in Korean custom response docs. PR [#15774](https://github.com/fastapi/fastapi/pull/15774) by [@kooqooo](https://github.com/kooqooo).
* 🌐 Update translations for fr (update-outdated). PR [#15761](https://github.com/fastapi/fastapi/pull/15761) by [@tiangolo](https://github.com/tiangolo).
* 🌐 Update translations for zh-hant (update-outdated). PR [#15760](https://github.com/fastapi/fastapi/pull/15760) by [@tiangolo](https://github.com/tiangolo).
* 🌐 Update translations for de (update-outdated). PR [#15759](https://github.com/fastapi/fastapi/pull/15759) by [@tiangolo](https://github.com/tiangolo).
* 🌐 Update translations for ko (update-outdated). PR [#15757](https://github.com/fastapi/fastapi/pull/15757) by [@tiangolo](https://github.com/tiangolo).
* 🌐 Update translations for uk (update-outdated). PR [#15756](https://github.com/fastapi/fastapi/pull/15756) by [@tiangolo](https://github.com/tiangolo).
* 🌐 Update translations for zh (update-outdated). PR [#15755](https://github.com/fastapi/fastapi/pull/15755) by [@tiangolo](https://github.com/tiangolo).
* 🌐 Update translations for tr (update-outdated). PR [#15754](https://github.com/fastapi/fastapi/pull/15754) by [@tiangolo](https://github.com/tiangolo).
* 🌐 Update translations for pt (update-outdated). PR [#15753](https://github.com/fastapi/fastapi/pull/15753) by [@tiangolo](https://github.com/tiangolo).
* 🌐 Update translations for es (update-outdated). PR [#15752](https://github.com/fastapi/fastapi/pull/15752) by [@tiangolo](https://github.com/tiangolo).
* 🌐 Update translations for ja (update-outdated). PR [#15751](https://github.com/fastapi/fastapi/pull/15751) by [@tiangolo](https://github.com/tiangolo).
* 🌐 Update translations for ru (update-outdated). PR [#15758](https://github.com/fastapi/fastapi/pull/15758) by [@tiangolo](https://github.com/tiangolo).

### Internal

* ⬆ Bump the python-packages group across 1 directory with 7 updates. PR [#15777](https://github.com/fastapi/fastapi/pull/15777) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump cryptography from 46.0.7 to 48.0.1. PR [#15779](https://github.com/fastapi/fastapi/pull/15779) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump aiohttp from 3.14.0 to 3.14.1. PR [#15781](https://github.com/fastapi/fastapi/pull/15781) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump starlette from 1.2.1 to 1.3.1. PR [#15780](https://github.com/fastapi/fastapi/pull/15780) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump astral-sh/setup-uv from 8.1.0 to 8.2.0 in the github-actions group. PR [#15776](https://github.com/fastapi/fastapi/pull/15776) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump https://github.com/crate-ci/typos from v1.47.1 to v1.47.2 in the pre-commit group. PR [#15775](https://github.com/fastapi/fastapi/pull/15775) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump python-multipart from 0.0.30 to 0.0.32. PR [#15778](https://github.com/fastapi/fastapi/pull/15778) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⏪️ Revert removing scripts, only remove `coverage.sh`. PR [#15772](https://github.com/fastapi/fastapi/pull/15772) by [@tiangolo](https://github.com/tiangolo).
* 🔥 Remove unused scripts. PR [#15771](https://github.com/fastapi/fastapi/pull/15771) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Add ty configs to check docs sources. PR [#15770](https://github.com/fastapi/fastapi/pull/15770) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Add ty configs to check docs sources. PR [#15769](https://github.com/fastapi/fastapi/pull/15769) by [@tiangolo](https://github.com/tiangolo).

## 0.137.1 (2026-06-15)

### Fixes

* 🚨 Fix typing checks for APIRoute. PR [#15765](https://github.com/fastapi/fastapi/pull/15765) by [@tiangolo](https://github.com/tiangolo).
* 🐛 Fix bug, allow empty path in path operation in prefixless router. PR [#15763](https://github.com/fastapi/fastapi/pull/15763) by [@tiangolo](https://github.com/tiangolo).

## 0.137.0 (2026-06-14)

### Breaking Changes

* ♻️ Refactor internals to preserve `APIRouter` and `APIRoute` instances. PR [#15745](https://github.com/fastapi/fastapi/pull/15745) by [@tiangolo](https://github.com/tiangolo).

Unblocks ✨ SO MANY THINGS ✨

Before this, `router.include_router(other_router)` would take each path operation from `other_router` and "clone" it, or recreate it from scratch.

This would mean that in the end there was only one top level router, part of the app.

The way it is structured here is that there are a few additional classes to handle intermediate metadata for router and route inclusion. That way the information of "router X includes Y and Y includes Z" is stored somewhere, without affecting (recreating / clonning) the final route.

#### Non Objectives

Dependencies for 404: previously I intended to support dependencies that would be executed even for 404, but that would conflict with the fact that a router could _not_ find a match, but the next router _did_ find a match. Executing dependencies in the router that did not find a match would not make sense, they could consume the request, body, etc. This original idea was discarded.

#### Specific Breaking Changes

Now `router.routes` is no longer a plain list of `APIRoute` objects, it can contain these intermediate objects that can contain additional routers, forming a tree.

Any logic that depended on iterating on the `router.routes` directly would be affected, that logic cannot expect to be able to extract data from a plain list of routes, as it's no longer a plain list but a tree.

Additionally, any logic that iterated on `router.routes` to modify them would now also see these new objects, and would not see all the routes in the app.

`router.routes` should be considered an internal implementation detail, only passed around to the FastAPI functions that need it.

#### Features

* Adding routes (path operations) after a router is included now works, they are reflected as they are not copied.
* Including `subrouter` in `mainrouter` can be done before adding routes (path operations) to `subrouter`, because now the the entire object is stored instead of copying the routes.
* As routes are not copied, in some cases that might save some memory.

#### Alpha Features

This is not documented yet, so it's not officially supported yet and could change in the future.

But, as `APIRoute` and `APIRouter` instances are now preserved, they could be customized.

`APIRouter` has two new methods, `.matches()` and `.handle()`, counterpart to the existing ones in `APIRoute`. With this a router could customize how it matches and handles requests. For example, it could match only requests that include some specific header, for example for handling versions in headers.

Still, for now, consider this very experimental and potentially changing and breaking in the future.

#### Future Features Enabled

* Custom `APIRoute` subclasses (undocumented, but alraedy works as desccribed above)
* Custom `APIRouter` subclasses (undocumented, but already works as described above)
* Dependencies per router
* Exception handlers per router
* Middleware per router
* Other features planned

### Docs

* 📝 Update release notes. PR [#15747](https://github.com/fastapi/fastapi/pull/15747) by [@tiangolo](https://github.com/tiangolo).
* 📝 Update FastAPI Cloud deployment instructions. PR [#15724](https://github.com/fastapi/fastapi/pull/15724) by [@alejsdev](https://github.com/alejsdev).
* ✏️ Use `Annotated` in inline example in `docs/en/docs/tutorial/body-multiple-params.md`. PR [#15591](https://github.com/fastapi/fastapi/pull/15591) by [@TheArchons](https://github.com/TheArchons).
* 📝 Remove "NGINX Unit" from the list of ASGI-servers in docs. PR [#15475](https://github.com/fastapi/fastapi/pull/15475) by [@angryfoxx](https://github.com/angryfoxx).
* 📝 Update `docs/en/docs/tutorial/security/oauth2-jwt.md`. PR [#14781](https://github.com/fastapi/fastapi/pull/14781) by [@zadevhub](https://github.com/zadevhub).

### Translations

* 🌐 Update translations for zh-hant (update-outdated). PR [#15671](https://github.com/fastapi/fastapi/pull/15671) by [@tiangolo](https://github.com/tiangolo).
* 🌐 Update translations for es (update-outdated). PR [#15670](https://github.com/fastapi/fastapi/pull/15670) by [@tiangolo](https://github.com/tiangolo).
* 🌐 Update translations for fr (update-outdated). PR [#15669](https://github.com/fastapi/fastapi/pull/15669) by [@tiangolo](https://github.com/tiangolo).
* 🌐 Update translations for ja (update-outdated). PR [#15668](https://github.com/fastapi/fastapi/pull/15668) by [@tiangolo](https://github.com/tiangolo).
* 🌐 Update translations for pt (update-outdated). PR [#15667](https://github.com/fastapi/fastapi/pull/15667) by [@tiangolo](https://github.com/tiangolo).
* 🌐 Update translations for tr (update-outdated). PR [#15666](https://github.com/fastapi/fastapi/pull/15666) by [@tiangolo](https://github.com/tiangolo).
* 🌐 Update translations for zh (update-outdated). PR [#15665](https://github.com/fastapi/fastapi/pull/15665) by [@tiangolo](https://github.com/tiangolo).
* 🌐 Update translations for ko (update-outdated). PR [#15664](https://github.com/fastapi/fastapi/pull/15664) by [@tiangolo](https://github.com/tiangolo).
* 🌐 Update translations for de (update-outdated). PR [#15673](https://github.com/fastapi/fastapi/pull/15673) by [@tiangolo](https://github.com/tiangolo).
* 🌐 Update translations for uk (update-outdated). PR [#15672](https://github.com/fastapi/fastapi/pull/15672) by [@tiangolo](https://github.com/tiangolo).
* 🌐 Update translations for ru (update-outdated). PR [#15674](https://github.com/fastapi/fastapi/pull/15674) by [@tiangolo](https://github.com/tiangolo).

### Internal

* 🔧 Update sponsors: remove TalorData. PR [#15744](https://github.com/fastapi/fastapi/pull/15744) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Update sponsors: remove ExoFlare. PR [#15736](https://github.com/fastapi/fastapi/pull/15736) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Update sponsors: remove InterviewPal. PR [#15735](https://github.com/fastapi/fastapi/pull/15735) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Update sponsors: remove Liblab. PR [#15731](https://github.com/fastapi/fastapi/pull/15731) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Update sponsors: remove Scalar. PR [#15730](https://github.com/fastapi/fastapi/pull/15730) by [@tiangolo](https://github.com/tiangolo).
* ⬆ Bump the python-packages group across 1 directory with 6 updates. PR [#15721](https://github.com/fastapi/fastapi/pull/15721) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump python-multipart from 0.0.29 to 0.0.30. PR [#15723](https://github.com/fastapi/fastapi/pull/15723) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump the github-actions group with 3 updates. PR [#15720](https://github.com/fastapi/fastapi/pull/15720) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump starlette from 1.1.0 to 1.2.1. PR [#15722](https://github.com/fastapi/fastapi/pull/15722) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump https://github.com/crate-ci/typos from v1.46.0 to v1.47.1 in the pre-commit group. PR [#15719](https://github.com/fastapi/fastapi/pull/15719) by [@dependabot[bot]](https://github.com/apps/dependabot).
* 🔧 Update sponsors, add Rapidproxy. PR [#15689](https://github.com/fastapi/fastapi/pull/15689) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Update sponsors: Remove TestMu. PR [#15688](https://github.com/fastapi/fastapi/pull/15688) by [@tiangolo](https://github.com/tiangolo).
* ⬆ Bump the python-packages group across 1 directory with 11 updates. PR [#15683](https://github.com/fastapi/fastapi/pull/15683) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump aiohttp from 3.13.4 to 3.14.0. PR [#15681](https://github.com/fastapi/fastapi/pull/15681) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump the github-actions group with 2 updates. PR [#15682](https://github.com/fastapi/fastapi/pull/15682) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump starlette from 1.0.0 to 1.1.0. PR [#15684](https://github.com/fastapi/fastapi/pull/15684) by [@dependabot[bot]](https://github.com/apps/dependabot).
* 👥 Update FastAPI People - Experts. PR [#15677](https://github.com/fastapi/fastapi/pull/15677) by [@tiangolo](https://github.com/tiangolo).
* 👥 Update FastAPI GitHub topic repositories. PR [#15675](https://github.com/fastapi/fastapi/pull/15675) by [@tiangolo](https://github.com/tiangolo).
* 👥 Update FastAPI People - Contributors and Translators. PR [#15662](https://github.com/fastapi/fastapi/pull/15662) by [@tiangolo](https://github.com/tiangolo).
* 👷 Automate release preparation. PR [#15661](https://github.com/fastapi/fastapi/pull/15661) by [@tiangolo](https://github.com/tiangolo).
* 🔥 Remove slim package stub, deprecated for a while. PR [#15649](https://github.com/fastapi/fastapi/pull/15649) by [@tiangolo](https://github.com/tiangolo).
* ⬆ Bump authlib from 1.6.11 to 1.7.2. PR [#15512](https://github.com/fastapi/fastapi/pull/15512) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump pymdown-extensions from 10.21.2 to 10.21.3. PR [#15569](https://github.com/fastapi/fastapi/pull/15569) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump CodSpeedHQ/action from 4.14.0 to 4.15.1. PR [#15513](https://github.com/fastapi/fastapi/pull/15513) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump python-multipart from 0.0.26 to 0.0.29. PR [#15595](https://github.com/fastapi/fastapi/pull/15595) by [@dependabot[bot]](https://github.com/apps/dependabot).
* 🔒️ Improve GitHub actions security. PR [#15607](https://github.com/fastapi/fastapi/pull/15607) by [@YuriiMotov](https://github.com/YuriiMotov).
* ⚰️ Remove ruff and coverage ignores for non-existing files. PR [#15610](https://github.com/fastapi/fastapi/pull/15610) by [@YuriiMotov](https://github.com/YuriiMotov).
* ✅ Use custom `changing_dir` instead of `CLIRunner.isolated_filesystem` to set working dir. PR [#15616](https://github.com/fastapi/fastapi/pull/15616) by [@YuriiMotov](https://github.com/YuriiMotov).
* ✅ Add `httpx2` test dependency to avoid deprecation warning. PR [#15603](https://github.com/fastapi/fastapi/pull/15603) by [@YuriiMotov](https://github.com/YuriiMotov).
* ⬆ Bump the python-packages group with 15 updates. PR [#15594](https://github.com/fastapi/fastapi/pull/15594) by [@dependabot[bot]](https://github.com/apps/dependabot).
* 👷 Configure Dependabot to group updates and update weekly. PR [#15560](https://github.com/fastapi/fastapi/pull/15560) by [@YuriiMotov](https://github.com/YuriiMotov).

## 0.136.3 (2026-05-23)

### Refactors

* ♻️ Do not accept underscore headers when using `convert_underscores=True` (the default). PR [#15589](https://github.com/fastapi/fastapi/pull/15589) by [@tiangolo](https://github.com/tiangolo).

## 0.136.2 (2026-05-23)

### Refactors

* ♻️ Validate Server Sent Event fields to avoid applications from sending broken data. PR [#15588](https://github.com/fastapi/fastapi/pull/15588) by [@tiangolo](https://github.com/tiangolo).

### Docs

* 📝 Document `--entrypoint` CLI option. PR [#15464](https://github.com/fastapi/fastapi/pull/15464) by [@YuriiMotov](https://github.com/YuriiMotov).
* 📝 Update and simplify docs about help and management. PR [#15583](https://github.com/fastapi/fastapi/pull/15583) by [@tiangolo](https://github.com/tiangolo).
* 📝 Add docs references to central contributing docs. PR [#15580](https://github.com/fastapi/fastapi/pull/15580) by [@tiangolo](https://github.com/tiangolo).
* 📝 Update security policy. PR [#15577](https://github.com/fastapi/fastapi/pull/15577) by [@tiangolo](https://github.com/tiangolo).
* 🍱 Update sponsors: TalorData image. PR [#15562](https://github.com/fastapi/fastapi/pull/15562) by [@tiangolo](https://github.com/tiangolo).
* 📝 Update docs, simplify usage of admonitions, only default ones. PR [#15553](https://github.com/fastapi/fastapi/pull/15553) by [@tiangolo](https://github.com/tiangolo).
* 📝 Fix image URLs in `index.md`. PR [#15534](https://github.com/fastapi/fastapi/pull/15534) by [@YuriiMotov](https://github.com/YuriiMotov).
* ✏️ Fix Azkaban spelling typo in `virtual-environments.md‎`. PR [#15463](https://github.com/fastapi/fastapi/pull/15463) by [@isaacbernat](https://github.com/isaacbernat).
* 💄 Improve layout and styling. PR [#15462](https://github.com/fastapi/fastapi/pull/15462) by [@alejsdev](https://github.com/alejsdev).
* 💄 Refactor opinions section with interactive tabs and new logos. PR [#15458](https://github.com/fastapi/fastapi/pull/15458) by [@alejsdev](https://github.com/alejsdev).
* 📝 Add FastAPI Conf '26 announcement to docs. PR [#15457](https://github.com/fastapi/fastapi/pull/15457) by [@alejsdev](https://github.com/alejsdev).

### Translations

* 🌐 Improve translation consistency in `‎docs/pt/docs/advanced/generate-clients.md‎`. PR [#15456](https://github.com/fastapi/fastapi/pull/15456) by [@Will-thom](https://github.com/Will-thom).
* 🌐 Update translations for ja (update-outdated). PR [#15530](https://github.com/fastapi/fastapi/pull/15530) by [@tiangolo](https://github.com/tiangolo).
* 🌐 Update translations for uk (update-outdated). PR [#15529](https://github.com/fastapi/fastapi/pull/15529) by [@tiangolo](https://github.com/tiangolo).
* 🌐 Update translations for pt (update-outdated). PR [#15528](https://github.com/fastapi/fastapi/pull/15528) by [@tiangolo](https://github.com/tiangolo).
* 🌐 Update translations for de (update-outdated). PR [#15527](https://github.com/fastapi/fastapi/pull/15527) by [@tiangolo](https://github.com/tiangolo).
* 🌐 Update translations for tr (update-outdated). PR [#15526](https://github.com/fastapi/fastapi/pull/15526) by [@tiangolo](https://github.com/tiangolo).
* 🌐 Update translations for ko (update-outdated). PR [#15525](https://github.com/fastapi/fastapi/pull/15525) by [@tiangolo](https://github.com/tiangolo).
* 🌐 Update translations for zh-hant (update-outdated). PR [#15524](https://github.com/fastapi/fastapi/pull/15524) by [@tiangolo](https://github.com/tiangolo).
* 🌐 Update translations for fr (update-outdated). PR [#15522](https://github.com/fastapi/fastapi/pull/15522) by [@tiangolo](https://github.com/tiangolo).
* 🌐 Update translations for es (update-outdated). PR [#15523](https://github.com/fastapi/fastapi/pull/15523) by [@tiangolo](https://github.com/tiangolo).
* 🌐 Update translations for zh (update-outdated). PR [#15520](https://github.com/fastapi/fastapi/pull/15520) by [@tiangolo](https://github.com/tiangolo).
* 🌐 Update translations for ru (update-outdated). PR [#15521](https://github.com/fastapi/fastapi/pull/15521) by [@tiangolo](https://github.com/tiangolo).
* 🌐 Fix typos in Spanish LLM-prompt. PR [#15472](https://github.com/fastapi/fastapi/pull/15472) by [@crr004](https://github.com/crr004).

### Internal

* ✅ Update tests, don't double dispose the engine. PR [#15587](https://github.com/fastapi/fastapi/pull/15587) by [@tiangolo](https://github.com/tiangolo).
* ⚡️ Speed up test suite via caching and fixture scopes to make it ~24% faster. PR [#13583](https://github.com/fastapi/fastapi/pull/13583) by [@dikos1337](https://github.com/dikos1337).
* 🔥 Remove config files now in central GitHub repo. PR [#15585](https://github.com/fastapi/fastapi/pull/15585) by [@tiangolo](https://github.com/tiangolo).
* ⬆ Bump urllib3 from 2.6.3 to 2.7.0. PR [#15502](https://github.com/fastapi/fastapi/pull/15502) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump idna from 3.11 to 3.15. PR [#15565](https://github.com/fastapi/fastapi/pull/15565) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump cloudflare/wrangler-action from 3.15.0 to 4.0.0. PR [#15571](https://github.com/fastapi/fastapi/pull/15571) by [@dependabot[bot]](https://github.com/apps/dependabot).
* 🔧 Migrate docs from MkDocs to Zensical. PR [#15563](https://github.com/fastapi/fastapi/pull/15563) by [@tiangolo](https://github.com/tiangolo).
* 🔒️ Only allow team members to modify dependencies. PR [#15548](https://github.com/fastapi/fastapi/pull/15548) by [@svlandeg](https://github.com/svlandeg).
* ⬆ Bump actions/add-to-project from 1.0.2 to 2.0.0. PR [#15490](https://github.com/fastapi/fastapi/pull/15490) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump actions/labeler from 6.0.1 to 6.1.0. PR [#15507](https://github.com/fastapi/fastapi/pull/15507) by [@dependabot[bot]](https://github.com/apps/dependabot).
* 🔧 Remove Ruff ignored rule for tabs. PR [#15533](https://github.com/fastapi/fastapi/pull/15533) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Update sponsors badge. PR [#15532](https://github.com/fastapi/fastapi/pull/15532) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Add sponsor: TalorData. PR [#15531](https://github.com/fastapi/fastapi/pull/15531) by [@tiangolo](https://github.com/tiangolo).
* ⬆ Bump ty from 0.0.21 to 0.0.34. PR [#15443](https://github.com/fastapi/fastapi/pull/15443) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump pydantic from 2.13.2 to 2.13.3. PR [#15444](https://github.com/fastapi/fastapi/pull/15444) by [@dependabot[bot]](https://github.com/apps/dependabot).
* 👷 Add pre-commit to check typos. PR [#15482](https://github.com/fastapi/fastapi/pull/15482) by [@tiangolo](https://github.com/tiangolo).
* 👥 Update FastAPI GitHub topic repositories. PR [#15470](https://github.com/fastapi/fastapi/pull/15470) by [@tiangolo](https://github.com/tiangolo).
* 👥 Update FastAPI People - Experts. PR [#15471](https://github.com/fastapi/fastapi/pull/15471) by [@tiangolo](https://github.com/tiangolo).
* 👥 Update FastAPI People - Contributors and Translators. PR [#15467](https://github.com/fastapi/fastapi/pull/15467) by [@tiangolo](https://github.com/tiangolo).
* 👷 Fix missing credentials issue in `translate` workflow. PR [#15468](https://github.com/fastapi/fastapi/pull/15468) by [@YuriiMotov](https://github.com/YuriiMotov).
* ⬆ Bump sqlmodel from 0.0.32 to 0.0.38. PR [#15437](https://github.com/fastapi/fastapi/pull/15437) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump CodSpeedHQ/action from 4.12.1 to 4.14.0. PR [#15436](https://github.com/fastapi/fastapi/pull/15436) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump pydantic from 2.12.5 to 2.13.2. PR [#15439](https://github.com/fastapi/fastapi/pull/15439) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump pydantic-ai from 1.63.0 to 1.83.0. PR [#15417](https://github.com/fastapi/fastapi/pull/15417) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump prek from 0.3.2 to 0.3.9. PR [#15418](https://github.com/fastapi/fastapi/pull/15418) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump fastar from 0.9.0 to 0.11.0. PR [#15419](https://github.com/fastapi/fastapi/pull/15419) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump astral-sh/setup-uv from 7.6.0 to 8.1.0. PR [#15415](https://github.com/fastapi/fastapi/pull/15415) by [@dependabot[bot]](https://github.com/apps/dependabot).

## 0.136.1 (2026-04-23)

### Upgrades

* ⬆️ Update Pydantic v2 code to address deprecations. PR [#15101](https://github.com/fastapi/fastapi/pull/15101) by [@svlandeg](https://github.com/svlandeg).

### Internal

* 🔨 Tweak translation script. PR [#15174](https://github.com/fastapi/fastapi/pull/15174) by [@YuriiMotov](https://github.com/YuriiMotov).
* ⬆ Bump mkdocs-material from 9.7.1 to 9.7.6. PR [#15408](https://github.com/fastapi/fastapi/pull/15408) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump inline-snapshot from 0.31.1 to 0.32.6. PR [#15409](https://github.com/fastapi/fastapi/pull/15409) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump pytest-codspeed from 4.3.0 to 4.4.0. PR [#15407](https://github.com/fastapi/fastapi/pull/15407) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump pytest-cov from 7.0.0 to 7.1.0. PR [#15406](https://github.com/fastapi/fastapi/pull/15406) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump cloudflare/wrangler-action from 3.14.1 to 3.15.0. PR [#15405](https://github.com/fastapi/fastapi/pull/15405) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump mypy from 1.19.1 to 1.20.1. PR [#15410](https://github.com/fastapi/fastapi/pull/15410) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump python-dotenv from 1.2.1 to 1.2.2. PR [#15400](https://github.com/fastapi/fastapi/pull/15400) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump starlette from 0.52.1 to 1.0.0. PR [#15397](https://github.com/fastapi/fastapi/pull/15397) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump pygithub from 2.8.1 to 2.9.1. PR [#15396](https://github.com/fastapi/fastapi/pull/15396) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump pyjwt from 2.12.0 to 2.12.1. PR [#15393](https://github.com/fastapi/fastapi/pull/15393) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump zizmor from 1.23.1 to 1.24.1. PR [#15394](https://github.com/fastapi/fastapi/pull/15394) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump strawberry-graphql from 0.312.3 to 0.314.3. PR [#15395](https://github.com/fastapi/fastapi/pull/15395) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump python-multipart from 0.0.22 to 0.0.26. PR [#15360](https://github.com/fastapi/fastapi/pull/15360) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump authlib from 1.6.9 to 1.6.11. PR [#15373](https://github.com/fastapi/fastapi/pull/15373) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump aiohttp from 3.13.3 to 3.13.4. PR [#15282](https://github.com/fastapi/fastapi/pull/15282) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump pygments from 2.19.2 to 2.20.0. PR [#15263](https://github.com/fastapi/fastapi/pull/15263) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump pymdown-extensions from 10.20.1 to 10.21.2. PR [#15391](https://github.com/fastapi/fastapi/pull/15391) by [@YuriiMotov](https://github.com/YuriiMotov).
* ⬆ Bump pillow from 12.1.1 to 12.2.0. PR [#15333](https://github.com/fastapi/fastapi/pull/15333) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump pytest from 9.0.2 to 9.0.3. PR [#15334](https://github.com/fastapi/fastapi/pull/15334) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump actions/upload-artifact from 7.0.0 to 7.0.1. PR [#15374](https://github.com/fastapi/fastapi/pull/15374) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump actions/cache from 5.0.4 to 5.0.5. PR [#15385](https://github.com/fastapi/fastapi/pull/15385) by [@dependabot[bot]](https://github.com/apps/dependabot).
* 🔧 Update sponsors: remove Zuplo. PR [#15369](https://github.com/fastapi/fastapi/pull/15369) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Update sponsors: remove Speakeasy. PR [#15368](https://github.com/fastapi/fastapi/pull/15368) by [@tiangolo](https://github.com/tiangolo).
* 🔒️ Add zizmor and fix audit findings. PR [#15316](https://github.com/fastapi/fastapi/pull/15316) by [@YuriiMotov](https://github.com/YuriiMotov).

## 0.136.0 (2026-04-16)

### Upgrades

* ⬆️ Support free-threaded Python 3.14t. PR [#15149](https://github.com/fastapi/fastapi/pull/15149) by [@svlandeg](https://github.com/svlandeg).

## 0.135.4 (2026-04-16)

### Refactors

* 🔥 Remove April Fool's `@app.vibe()` 🤪. PR [#15363](https://github.com/fastapi/fastapi/pull/15363) by [@tiangolo](https://github.com/tiangolo).

### Internal

* ⬆ Bump cryptography from 46.0.5 to 46.0.7. PR [#15314](https://github.com/fastapi/fastapi/pull/15314) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump strawberry-graphql from 0.307.1 to 0.312.3. PR [#15309](https://github.com/fastapi/fastapi/pull/15309) by [@dependabot[bot]](https://github.com/apps/dependabot).
* 🔨 Add pre-commit hook to ensure latest release header has date. PR [#15293](https://github.com/fastapi/fastapi/pull/15293) by [@YuriiMotov](https://github.com/YuriiMotov).

## 0.135.3 (2026-04-01)

### Features

* ✨ Add support for `@app.vibe()`. PR [#15280](https://github.com/fastapi/fastapi/pull/15280) by [@tiangolo](https://github.com/tiangolo).
    * New docs: [Vibe Coding](https://fastapi.tiangolo.com/advanced/vibe/).

### Docs

* ✏️ Fix typo for `client_secret` in OAuth2 form docstrings. PR [#14946](https://github.com/fastapi/fastapi/pull/14946) by [@bysiber](https://github.com/bysiber).

### Internal

* 👥 Update FastAPI People - Experts. PR [#15279](https://github.com/fastapi/fastapi/pull/15279) by [@tiangolo](https://github.com/tiangolo).
* ⬆ Bump orjson from 3.11.7 to 3.11.8. PR [#15276](https://github.com/fastapi/fastapi/pull/15276) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump ruff from 0.15.0 to 0.15.8. PR [#15277](https://github.com/fastapi/fastapi/pull/15277) by [@dependabot[bot]](https://github.com/apps/dependabot).
* 👥 Update FastAPI GitHub topic repositories. PR [#15274](https://github.com/fastapi/fastapi/pull/15274) by [@tiangolo](https://github.com/tiangolo).
* ⬆ Bump fastmcp from 2.14.5 to 3.2.0. PR [#15267](https://github.com/fastapi/fastapi/pull/15267) by [@dependabot[bot]](https://github.com/apps/dependabot).
* 👥 Update FastAPI People - Contributors and Translators. PR [#15270](https://github.com/fastapi/fastapi/pull/15270) by [@tiangolo](https://github.com/tiangolo).
* ⬆ Bump requests from 2.32.5 to 2.33.0. PR [#15228](https://github.com/fastapi/fastapi/pull/15228) by [@dependabot[bot]](https://github.com/apps/dependabot).
* 👷 Add ty check to `lint.sh`. PR [#15136](https://github.com/fastapi/fastapi/pull/15136) by [@svlandeg](https://github.com/svlandeg).

## 0.135.2 (2026-03-01)

### Upgrades

* ⬆️ Increase lower bound to `pydantic >=2.9.0.` and fix the test suite. PR [#15139](https://github.com/fastapi/fastapi/pull/15139) by [@svlandeg](https://github.com/svlandeg).

### Docs

* 📝 Add missing last release notes dates. PR [#15202](https://github.com/fastapi/fastapi/pull/15202) by [@tiangolo](https://github.com/tiangolo).
* 📝 Update docs for contributors and team members regarding translation PRs. PR [#15200](https://github.com/fastapi/fastapi/pull/15200) by [@YuriiMotov](https://github.com/YuriiMotov).
* 💄 Fix code blocks in reference docs overflowing table width. PR [#15094](https://github.com/fastapi/fastapi/pull/15094) by [@YuriiMotov](https://github.com/YuriiMotov).
* 📝 Fix duplicated words in docstrings. PR [#15116](https://github.com/fastapi/fastapi/pull/15116) by [@AhsanSheraz](https://github.com/AhsanSheraz).
* 📝 Add docs for `pyproject.toml` with `entrypoint`. PR [#15075](https://github.com/fastapi/fastapi/pull/15075) by [@tiangolo](https://github.com/tiangolo).
* 📝 Update links in docs to no longer use the classes external-link and internal-link. PR [#15061](https://github.com/fastapi/fastapi/pull/15061) by [@tiangolo](https://github.com/tiangolo).
* 🔨 Add JS and CSS handling for automatic `target=_blank` for links in docs. PR [#15063](https://github.com/fastapi/fastapi/pull/15063) by [@tiangolo](https://github.com/tiangolo).
* 💄 Update styles for internal and external links in new tab. PR [#15058](https://github.com/fastapi/fastapi/pull/15058) by [@tiangolo](https://github.com/tiangolo).
* 📝  Add documentation for the FastAPI VS Code extension. PR [#15008](https://github.com/fastapi/fastapi/pull/15008) by [@savannahostrowski](https://github.com/savannahostrowski).
* 📝 Fix doctrings for `max_digits` and `decimal_places`. PR [#14944](https://github.com/fastapi/fastapi/pull/14944) by [@YuriiMotov](https://github.com/YuriiMotov).
* 📝 Add dates to release notes. PR [#15001](https://github.com/fastapi/fastapi/pull/15001) by [@YuriiMotov](https://github.com/YuriiMotov).

### Translations

* 🌐 Update translations for zh (update-outdated). PR [#15177](https://github.com/fastapi/fastapi/pull/15177) by [@tiangolo](https://github.com/tiangolo).
* 🌐 Update translations for zh-hant (update-outdated). PR [#15178](https://github.com/fastapi/fastapi/pull/15178) by [@tiangolo](https://github.com/tiangolo).
* 🌐 Update translations for zh-hant (add-missing). PR [#15176](https://github.com/fastapi/fastapi/pull/15176) by [@tiangolo](https://github.com/tiangolo).
* 🌐 Update translations for zh (add-missing). PR [#15175](https://github.com/fastapi/fastapi/pull/15175) by [@tiangolo](https://github.com/tiangolo).
* 🌐 Update translations for ja (update-outdated). PR [#15171](https://github.com/fastapi/fastapi/pull/15171) by [@tiangolo](https://github.com/tiangolo).
* 🌐 Update translations for ko (update-outdated). PR [#15170](https://github.com/fastapi/fastapi/pull/15170) by [@tiangolo](https://github.com/tiangolo).
* 🌐 Update translations for tr (update-outdated). PR [#15172](https://github.com/fastapi/fastapi/pull/15172) by [@tiangolo](https://github.com/tiangolo).
* 🌐 Update translations for ko (add-missing). PR [#15168](https://github.com/fastapi/fastapi/pull/15168) by [@tiangolo](https://github.com/tiangolo).
* 🌐 Update translations for ja (add-missing). PR [#15167](https://github.com/fastapi/fastapi/pull/15167) by [@tiangolo](https://github.com/tiangolo).
* 🌐 Update translations for tr (add-missing). PR [#15169](https://github.com/fastapi/fastapi/pull/15169) by [@tiangolo](https://github.com/tiangolo).
* 🌐 Update translations for fr (update-outdated). PR [#15165](https://github.com/fastapi/fastapi/pull/15165) by [@tiangolo](https://github.com/tiangolo).
* 🌐 Update translations for fr (add-missing). PR [#15163](https://github.com/fastapi/fastapi/pull/15163) by [@tiangolo](https://github.com/tiangolo).
* 🌐 Update translations for uk (update-outdated). PR [#15160](https://github.com/fastapi/fastapi/pull/15160) by [@tiangolo](https://github.com/tiangolo).
* 🌐 Update translations for uk (add-missing). PR [#15158](https://github.com/fastapi/fastapi/pull/15158) by [@tiangolo](https://github.com/tiangolo).
* 🌐 Update translations for pt (add-missing). PR [#15157](https://github.com/fastapi/fastapi/pull/15157) by [@tiangolo](https://github.com/tiangolo).
* 🌐 Update translations for pt (update-outdated). PR [#15159](https://github.com/fastapi/fastapi/pull/15159) by [@tiangolo](https://github.com/tiangolo).
* 🌐 Update translations for es (update-outdated). PR [#15155](https://github.com/fastapi/fastapi/pull/15155) by [@tiangolo](https://github.com/tiangolo).
* 🌐 Update translations for es (add-missing). PR [#15154](https://github.com/fastapi/fastapi/pull/15154) by [@tiangolo](https://github.com/tiangolo).
* 🌐 Update translations for de (update-outdated). PR [#15156](https://github.com/fastapi/fastapi/pull/15156) by [@tiangolo](https://github.com/tiangolo).
* 🌐 Update translations for ru (update-and-add). PR [#15152](https://github.com/fastapi/fastapi/pull/15152) by [@tiangolo](https://github.com/tiangolo).
* 🌐 Update translations for de (add-missing). PR [#15153](https://github.com/fastapi/fastapi/pull/15153) by [@tiangolo](https://github.com/tiangolo).

### Internal

* 🔨 Exclude spam comments from statistics in `scripts/people.py`. PR [#15088](https://github.com/fastapi/fastapi/pull/15088) by [@YuriiMotov](https://github.com/YuriiMotov).
* ⬆ Bump authlib from 1.6.7 to 1.6.9. PR [#15128](https://github.com/fastapi/fastapi/pull/15128) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump pyasn1 from 0.6.2 to 0.6.3. PR [#15143](https://github.com/fastapi/fastapi/pull/15143) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump ujson from 5.11.0 to 5.12.0. PR [#15150](https://github.com/fastapi/fastapi/pull/15150) by [@dependabot[bot]](https://github.com/apps/dependabot).
* 🔨 Tweak translation workflow and translation fixer tool. PR [#15166](https://github.com/fastapi/fastapi/pull/15166) by [@YuriiMotov](https://github.com/YuriiMotov).
* 🔨 Fix `commit_in_place` passed via env variable in `translate.yml` workflow. PR [#15151](https://github.com/fastapi/fastapi/pull/15151) by [@YuriiMotov](https://github.com/YuriiMotov).
* 🔨 Update translation general prompt to enforce link style in translation matches the original link style. PR [#15148](https://github.com/fastapi/fastapi/pull/15148) by [@YuriiMotov](https://github.com/YuriiMotov).
* 👷 Re-enable translation workflow run by cron in CI (twice a month). PR [#15145](https://github.com/fastapi/fastapi/pull/15145) by [@YuriiMotov](https://github.com/YuriiMotov).
* 👷 Add `ty` to precommit. PR [#15091](https://github.com/fastapi/fastapi/pull/15091) by [@svlandeg](https://github.com/svlandeg).
* ⬆ Bump dorny/paths-filter from 3 to 4. PR [#15106](https://github.com/fastapi/fastapi/pull/15106) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump cairosvg from 2.8.2 to 2.9.0. PR [#15108](https://github.com/fastapi/fastapi/pull/15108) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump pyjwt from 2.11.0 to 2.12.0. PR [#15110](https://github.com/fastapi/fastapi/pull/15110) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump black from 26.1.0 to 26.3.1. PR [#15100](https://github.com/fastapi/fastapi/pull/15100) by [@dependabot[bot]](https://github.com/apps/dependabot).
* 🔨 Update script to autofix permalinks to account for headers with Markdown links. PR [#15062](https://github.com/fastapi/fastapi/pull/15062) by [@tiangolo](https://github.com/tiangolo).
* 📌 Pin Click for MkDocs live reload. PR [#15057](https://github.com/fastapi/fastapi/pull/15057) by [@tiangolo](https://github.com/tiangolo).
* ⬆ Bump werkzeug from 3.1.5 to 3.1.6. PR [#14948](https://github.com/fastapi/fastapi/pull/14948) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump pydantic-ai from 1.62.0 to 1.63.0. PR [#15035](https://github.com/fastapi/fastapi/pull/15035) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump pytest-codspeed from 4.2.0 to 4.3.0. PR [#15034](https://github.com/fastapi/fastapi/pull/15034) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump strawberry-graphql from 0.291.2 to 0.307.1. PR [#15033](https://github.com/fastapi/fastapi/pull/15033) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump typer from 0.21.1 to 0.24.1. PR [#15032](https://github.com/fastapi/fastapi/pull/15032) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump actions/download-artifact from 7 to 8. PR [#15020](https://github.com/fastapi/fastapi/pull/15020) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump actions/upload-artifact from 6 to 7. PR [#15019](https://github.com/fastapi/fastapi/pull/15019) by [@dependabot[bot]](https://github.com/apps/dependabot).

## 0.135.1 (2026-03-01)

### Fixes

* 🐛 Fix, avoid yield from a TaskGroup, only as an async context manager, closed in the request async exit stack. PR [#15038](https://github.com/fastapi/fastapi/pull/15038) by [@tiangolo](https://github.com/tiangolo).

### Docs

* ✏️ Fix typo in `docs/en/docs/_llm-test.md`. PR [#15007](https://github.com/fastapi/fastapi/pull/15007) by [@adityagiri3600](https://github.com/adityagiri3600).
* 📝 Update Skill, optimize context, trim and refactor into references. PR [#15031](https://github.com/fastapi/fastapi/pull/15031) by [@tiangolo](https://github.com/tiangolo).

### Internal

* 👥 Update FastAPI People - Experts. PR [#15037](https://github.com/fastapi/fastapi/pull/15037) by [@tiangolo](https://github.com/tiangolo).
* 👥 Update FastAPI People - Contributors and Translators. PR [#15029](https://github.com/fastapi/fastapi/pull/15029) by [@tiangolo](https://github.com/tiangolo).
* 👥 Update FastAPI GitHub topic repositories. PR [#15036](https://github.com/fastapi/fastapi/pull/15036) by [@tiangolo](https://github.com/tiangolo).

## 0.135.0 (2026-03-01)

### Features

* ✨ Add support for Server Sent Events. PR [#15030](https://github.com/fastapi/fastapi/pull/15030) by [@tiangolo](https://github.com/tiangolo).
    * New docs: [Server-Sent Events (SSE)](https://fastapi.tiangolo.com/tutorial/server-sent-events/).

## 0.134.0 (2026-02-27)

### Features

* ✨ Add support for streaming JSON Lines and binary data with `yield`. PR [#15022](https://github.com/fastapi/fastapi/pull/15022) by [@tiangolo](https://github.com/tiangolo).
    * This also upgrades Starlette from `>=0.40.0` to `>=0.46.0`, as it's needed to properly unrwap and re-raise exceptions from exception groups.
    * New docs: [Stream JSON Lines](https://fastapi.tiangolo.com/tutorial/stream-json-lines/).
    * And new docs: [Stream Data](https://fastapi.tiangolo.com/advanced/stream-data/).

### Docs

* 📝 Update Library Agent Skill with streaming responses. PR [#15024](https://github.com/fastapi/fastapi/pull/15024) by [@tiangolo](https://github.com/tiangolo).
* 📝 Update docs for responses and new stream with `yield`. PR [#15023](https://github.com/fastapi/fastapi/pull/15023) by [@tiangolo](https://github.com/tiangolo).
* 📝 Add `await` in `StreamingResponse` code example to allow cancellation. PR [#14681](https://github.com/fastapi/fastapi/pull/14681) by [@casperdcl](https://github.com/casperdcl).
* 📝 Rename `docs_src/websockets` to `docs_src/websockets_` to avoid import errors. PR [#14979](https://github.com/fastapi/fastapi/pull/14979) by [@YuriiMotov](https://github.com/YuriiMotov).

### Internal

* 🔨 Run tests with `pytest-xdist` and `pytest-cov`. PR [#14992](https://github.com/fastapi/fastapi/pull/14992) by [@YuriiMotov](https://github.com/YuriiMotov).

## 0.133.1 (2026-02-25)

### Features

* 🔧 Add FastAPI Agents Skill. PR [#14982](https://github.com/fastapi/fastapi/pull/14982) by [@tiangolo](https://github.com/tiangolo).
    * Read more about it in [Library Agent Skills](https://tiangolo.com/ideas/library-agent-skills/).

### Internal

* ✅ Fix all tests are skipped on Windows. PR [#14994](https://github.com/fastapi/fastapi/pull/14994) by [@YuriiMotov](https://github.com/YuriiMotov).

## 0.133.0 (2026-02-24)

### Upgrades

* ⬆️ Add support for Starlette 1.0.0+. PR [#14987](https://github.com/fastapi/fastapi/pull/14987) by [@tiangolo](https://github.com/tiangolo).

## 0.132.1 (2026-02-24)

### Refactors

* ♻️ Refactor logic to handle OpenAPI and Swagger UI escaping data. PR [#14986](https://github.com/fastapi/fastapi/pull/14986) by [@tiangolo](https://github.com/tiangolo).

### Internal

* 👥 Update FastAPI People - Experts. PR [#14972](https://github.com/fastapi/fastapi/pull/14972) by [@tiangolo](https://github.com/tiangolo).
* 👷 Allow skipping `benchmark` job in `test` workflow. PR [#14974](https://github.com/fastapi/fastapi/pull/14974) by [@YuriiMotov](https://github.com/YuriiMotov).

## 0.132.0 (2026-02-23)

### Breaking Changes

* 🔒️ Add `strict_content_type` checking for JSON requests. PR [#14978](https://github.com/fastapi/fastapi/pull/14978) by [@tiangolo](https://github.com/tiangolo).
    * Now FastAPI checks, by default, that JSON requests have a `Content-Type` header with a valid JSON value, like `application/json`, and rejects requests that don't.
    * If the clients for your app don't send a valid `Content-Type` header you can disable this with `strict_content_type=False`.
    * Check the new docs: [Strict Content-Type Checking](https://fastapi.tiangolo.com/advanced/strict-content-type/).

### Internal

* ⬆ Bump flask from 3.1.2 to 3.1.3. PR [#14949](https://github.com/fastapi/fastapi/pull/14949) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Update all dependencies to use `griffelib` instead of `griffe`. PR [#14973](https://github.com/fastapi/fastapi/pull/14973) by [@svlandeg](https://github.com/svlandeg).
* 🔨 Fix `FastAPI People` workflow. PR [#14951](https://github.com/fastapi/fastapi/pull/14951) by [@YuriiMotov](https://github.com/YuriiMotov).
* 👷 Do not run codspeed with coverage as it's not tracked. PR [#14966](https://github.com/fastapi/fastapi/pull/14966) by [@tiangolo](https://github.com/tiangolo).
* 👷 Do not include benchmark tests in coverage to speed up coverage processing. PR [#14965](https://github.com/fastapi/fastapi/pull/14965) by [@tiangolo](https://github.com/tiangolo).

## 0.131.0 (2026-02-22)

### Breaking Changes

* 🗑️ Deprecate `ORJSONResponse` and `UJSONResponse`. PR [#14964](https://github.com/fastapi/fastapi/pull/14964) by [@tiangolo](https://github.com/tiangolo).

## 0.130.0 (2026-02-22)

### Features

* ✨ Serialize JSON response with Pydantic (in Rust), when there's a Pydantic return type or response model. PR [#14962](https://github.com/fastapi/fastapi/pull/14962) by [@tiangolo](https://github.com/tiangolo).
    * This results in 2x (or more) performance increase for JSON responses.
    * New docs: [Custom Response - JSON Performance](https://fastapi.tiangolo.com/advanced/custom-response/#json-performance).

## 0.129.2 (2026-02-21)

### Internal

* ⬆️ Upgrade pytest. PR [#14959](https://github.com/fastapi/fastapi/pull/14959) by [@tiangolo](https://github.com/tiangolo).
* 👷 Fix CI, do not attempt to publish `fastapi-slim`. PR [#14958](https://github.com/fastapi/fastapi/pull/14958) by [@tiangolo](https://github.com/tiangolo).
* ➖ Drop support for `fastapi-slim`, no more versions will be released, use only `"fastapi[standard]"` or `fastapi`. PR [#14957](https://github.com/fastapi/fastapi/pull/14957) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Update pyproject.toml, remove unneeded lines. PR [#14956](https://github.com/fastapi/fastapi/pull/14956) by [@tiangolo](https://github.com/tiangolo).

## 0.129.1 (2026-02-21)

### Fixes

* ♻️ Fix JSON Schema for bytes, use `"contentMediaType": "application/octet-stream"` instead of `"format": "binary"`. PR [#14953](https://github.com/fastapi/fastapi/pull/14953) by [@tiangolo](https://github.com/tiangolo).

### Docs

* 🔨 Add Kapa.ai widget (AI chatbot). PR [#14938](https://github.com/fastapi/fastapi/pull/14938) by [@tiangolo](https://github.com/tiangolo).
* 🔥 Remove Python 3.9 specific files, no longer needed after updating translations. PR [#14931](https://github.com/fastapi/fastapi/pull/14931) by [@tiangolo](https://github.com/tiangolo).
* 📝 Update docs for JWT to prevent timing attacks. PR [#14908](https://github.com/fastapi/fastapi/pull/14908) by [@tiangolo](https://github.com/tiangolo).

### Translations

* ✏️ Fix several typos in ru translations. PR [#14934](https://github.com/fastapi/fastapi/pull/14934) by [@argoarsiks](https://github.com/argoarsiks).
* 🌐 Update translations for ko (update-all and add-missing). PR [#14923](https://github.com/fastapi/fastapi/pull/14923) by [@YuriiMotov](https://github.com/YuriiMotov).
* 🌐 Update translations for uk (add-missing). PR [#14922](https://github.com/fastapi/fastapi/pull/14922) by [@YuriiMotov](https://github.com/YuriiMotov).
* 🌐 Update translations for zh-hant (update-all and add-missing). PR [#14921](https://github.com/fastapi/fastapi/pull/14921) by [@YuriiMotov](https://github.com/YuriiMotov).
* 🌐 Update translations for fr (update-all and add-missing). PR [#14920](https://github.com/fastapi/fastapi/pull/14920) by [@YuriiMotov](https://github.com/YuriiMotov).
* 🌐 Update translations for de (update-all) . PR [#14910](https://github.com/fastapi/fastapi/pull/14910) by [@YuriiMotov](https://github.com/YuriiMotov).
* 🌐 Update translations for ja (update-all). PR [#14916](https://github.com/fastapi/fastapi/pull/14916) by [@YuriiMotov](https://github.com/YuriiMotov).
* 🌐 Update translations for pt (update-all). PR [#14912](https://github.com/fastapi/fastapi/pull/14912) by [@YuriiMotov](https://github.com/YuriiMotov).
* 🌐 Update translations for es (update-all and add-missing). PR [#14911](https://github.com/fastapi/fastapi/pull/14911) by [@YuriiMotov](https://github.com/YuriiMotov).
* 🌐 Update translations for zh (update-all). PR [#14917](https://github.com/fastapi/fastapi/pull/14917) by [@YuriiMotov](https://github.com/YuriiMotov).
* 🌐 Update translations for uk (update-all). PR [#14914](https://github.com/fastapi/fastapi/pull/14914) by [@YuriiMotov](https://github.com/YuriiMotov).
* 🌐 Update translations for tr (update-all). PR [#14913](https://github.com/fastapi/fastapi/pull/14913) by [@YuriiMotov](https://github.com/YuriiMotov).
* 🌐 Update translations for ru (update-outdated). PR [#14909](https://github.com/fastapi/fastapi/pull/14909) by [@YuriiMotov](https://github.com/YuriiMotov).

### Internal

* 👷 Always run tests on push to `master` branch and when run by scheduler. PR [#14940](https://github.com/fastapi/fastapi/pull/14940) by [@YuriiMotov](https://github.com/YuriiMotov).
* 🎨 Upgrade typing syntax for Python 3.10. PR [#14932](https://github.com/fastapi/fastapi/pull/14932) by [@tiangolo](https://github.com/tiangolo).
* ⬆ Bump cryptography from 46.0.4 to 46.0.5. PR [#14892](https://github.com/fastapi/fastapi/pull/14892) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump pillow from 12.1.0 to 12.1.1. PR [#14899](https://github.com/fastapi/fastapi/pull/14899) by [@dependabot[bot]](https://github.com/apps/dependabot).

## 0.129.0 (2026-02-12)

### Breaking Changes

* ➖ Drop support for Python 3.9. PR [#14897](https://github.com/fastapi/fastapi/pull/14897) by [@tiangolo](https://github.com/tiangolo).

### Refactors

* 🎨 Update internal types for Python 3.10. PR [#14898](https://github.com/fastapi/fastapi/pull/14898) by [@tiangolo](https://github.com/tiangolo).

### Docs

* 📝 Update highlights in webhooks docs. PR [#14905](https://github.com/fastapi/fastapi/pull/14905) by [@tiangolo](https://github.com/tiangolo).
* 📝 Update source examples and docs from Python 3.9 to 3.10. PR [#14900](https://github.com/fastapi/fastapi/pull/14900) by [@tiangolo](https://github.com/tiangolo).

### Internal

* 🔨 Update docs.py scripts to migrate Python 3.9 to Python 3.10. PR [#14906](https://github.com/fastapi/fastapi/pull/14906) by [@tiangolo](https://github.com/tiangolo).

## 0.128.8 (2026-02-11)

### Docs

* 📝 Fix grammar in `docs/en/docs/tutorial/first-steps.md`. PR [#14708](https://github.com/fastapi/fastapi/pull/14708) by [@SanjanaS10](https://github.com/SanjanaS10).

### Internal

* 🔨 Tweak PDM hook script. PR [#14895](https://github.com/fastapi/fastapi/pull/14895) by [@tiangolo](https://github.com/tiangolo).
* ♻️ Update build setup for `fastapi-slim`, deprecate it, and make it only depend on `fastapi`. PR [#14894](https://github.com/fastapi/fastapi/pull/14894) by [@tiangolo](https://github.com/tiangolo).

## 0.128.7 (2026-02-10)

### Features

* ✨ Show a clear error on attempt to include router into itself. PR [#14258](https://github.com/fastapi/fastapi/pull/14258) by [@JavierSanchezCastro](https://github.com/JavierSanchezCastro).
* ✨ Replace `dict` by `Mapping` on `HTTPException.headers`. PR [#12997](https://github.com/fastapi/fastapi/pull/12997) by [@rijenkii](https://github.com/rijenkii).

### Refactors

* ♻️ Simplify reading files in memory, do it sequentially instead of (fake) parallel. PR [#14884](https://github.com/fastapi/fastapi/pull/14884) by [@tiangolo](https://github.com/tiangolo).

### Docs

* 📝 Use `dfn` tag for definitions instead of `abbr` in docs. PR [#14744](https://github.com/fastapi/fastapi/pull/14744) by [@YuriiMotov](https://github.com/YuriiMotov).

### Internal

* ✅ Tweak comment in test to reference PR. PR [#14885](https://github.com/fastapi/fastapi/pull/14885) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Update LLM-prompt for `abbr` and `dfn` tags. PR [#14747](https://github.com/fastapi/fastapi/pull/14747) by [@YuriiMotov](https://github.com/YuriiMotov).
* ✅ Test order for the submitted byte Files. PR [#14828](https://github.com/fastapi/fastapi/pull/14828) by [@valentinDruzhinin](https://github.com/valentinDruzhinin).
* 🔧 Configure `test` workflow to run tests with `inline-snapshot=review`. PR [#14876](https://github.com/fastapi/fastapi/pull/14876) by [@YuriiMotov](https://github.com/YuriiMotov).

## 0.128.6 (2026-02-09)

### Fixes

* 🐛 Fix `on_startup` and `on_shutdown` parameters of `APIRouter`. PR [#14873](https://github.com/fastapi/fastapi/pull/14873) by [@YuriiMotov](https://github.com/YuriiMotov).

### Translations

* 🌐 Update translations for zh (update-outdated). PR [#14843](https://github.com/fastapi/fastapi/pull/14843) by [@tiangolo](https://github.com/tiangolo).

### Internal

* ✅ Fix parameterized tests with snapshots. PR [#14875](https://github.com/fastapi/fastapi/pull/14875) by [@YuriiMotov](https://github.com/YuriiMotov).

## 0.128.5 (2026-02-08)

### Refactors

* ♻️ Refactor and simplify Pydantic v2 (and v1) compatibility internal utils. PR [#14862](https://github.com/fastapi/fastapi/pull/14862) by [@tiangolo](https://github.com/tiangolo).

### Internal

* ✅ Add inline snapshot tests for OpenAPI before changes from Pydantic v2. PR [#14864](https://github.com/fastapi/fastapi/pull/14864) by [@tiangolo](https://github.com/tiangolo).

## 0.128.4 (2026-02-07)

### Refactors

* ♻️ Refactor internals, simplify Pydantic v2/v1 utils, `create_model_field`, better types for `lenient_issubclass`. PR [#14860](https://github.com/fastapi/fastapi/pull/14860) by [@tiangolo](https://github.com/tiangolo).
* ♻️ Simplify internals, remove Pydantic v1 only logic, no longer needed. PR [#14857](https://github.com/fastapi/fastapi/pull/14857) by [@tiangolo](https://github.com/tiangolo).
* ♻️ Refactor internals, cleanup unneeded Pydantic v1 specific logic. PR [#14856](https://github.com/fastapi/fastapi/pull/14856) by [@tiangolo](https://github.com/tiangolo).

### Translations

* 🌐 Update translations for fr (outdated pages). PR [#14839](https://github.com/fastapi/fastapi/pull/14839) by [@YuriiMotov](https://github.com/YuriiMotov).
* 🌐 Update translations for tr (outdated and missing). PR [#14838](https://github.com/fastapi/fastapi/pull/14838) by [@YuriiMotov](https://github.com/YuriiMotov).

### Internal

* ⬆️ Upgrade development dependencies. PR [#14854](https://github.com/fastapi/fastapi/pull/14854) by [@tiangolo](https://github.com/tiangolo).

## 0.128.3 (2026-02-06)

### Refactors

* ♻️ Re-implement `on_event` in FastAPI for compatibility with the next Starlette, while keeping backwards compatibility. PR [#14851](https://github.com/fastapi/fastapi/pull/14851) by [@tiangolo](https://github.com/tiangolo).

### Upgrades

* ⬆️ Upgrade Starlette supported version range to `starlette>=0.40.0,=5.8.0`, `orjson >=3.9.3`. PR [#14846](https://github.com/fastapi/fastapi/pull/14846) by [@tiangolo](https://github.com/tiangolo).

## 0.128.2 (2026-02-05)

### Features

* ✨ Add support for PEP695 `TypeAliasType`. PR [#13920](https://github.com/fastapi/fastapi/pull/13920) by [@cstruct](https://github.com/cstruct).
* ✨ Allow `Response` type hint as dependency annotation. PR [#14794](https://github.com/fastapi/fastapi/pull/14794) by [@jonathan-fulton](https://github.com/jonathan-fulton).

### Fixes

* 🐛 Fix using `Json[list[str]]` type (issue #10997). PR [#14616](https://github.com/fastapi/fastapi/pull/14616) by [@mkanetsuna](https://github.com/mkanetsuna).

### Docs

* 📝 Update docs for translations. PR [#14830](https://github.com/fastapi/fastapi/pull/14830) by [@tiangolo](https://github.com/tiangolo).
* 📝 Fix duplicate word in `advanced-dependencies.md`. PR [#14815](https://github.com/fastapi/fastapi/pull/14815) by [@Rayyan-Oumlil](https://github.com/Rayyan-Oumlil).

### Translations

* 🌐 Enable Traditional Chinese translations. PR [#14842](https://github.com/fastapi/fastapi/pull/14842) by [@tiangolo](https://github.com/tiangolo).
* 🌐 Enable French docs translations. PR [#14841](https://github.com/fastapi/fastapi/pull/14841) by [@tiangolo](https://github.com/tiangolo).
* 🌐 Update translations for fr (translate-page). PR [#14837](https://github.com/fastapi/fastapi/pull/14837) by [@tiangolo](https://github.com/tiangolo).
* 🌐 Update translations for de (update-outdated). PR [#14836](https://github.com/fastapi/fastapi/pull/14836) by [@tiangolo](https://github.com/tiangolo).
* 🌐 Update translations for pt (update-outdated). PR [#14833](https://github.com/fastapi/fastapi/pull/14833) by [@tiangolo](https://github.com/tiangolo).
* 🌐 Update translations for ko (update-outdated). PR [#14835](https://github.com/fastapi/fastapi/pull/14835) by [@tiangolo](https://github.com/tiangolo).
* 🌐 Update translations for es (update-outdated). PR [#14832](https://github.com/fastapi/fastapi/pull/14832) by [@tiangolo](https://github.com/tiangolo).
* 🌐 Update translations for tr (update-outdated). PR [#14831](https://github.com/fastapi/fastapi/pull/14831) by [@tiangolo](https://github.com/tiangolo).
* 🌐 Update translations for tr (add-missing). PR [#14790](https://github.com/fastapi/fastapi/pull/14790) by [@tiangolo](https://github.com/tiangolo).
* 🌐 Update translations for fr (update-outdated). PR [#14826](https://github.com/fastapi/fastapi/pull/14826) by [@tiangolo](https://github.com/tiangolo).
* 🌐 Update translations for zh-hant (update-outdated). PR [#14825](https://github.com/fastapi/fastapi/pull/14825) by [@tiangolo](https://github.com/tiangolo).
* 🌐 Update translations for uk (update-outdated). PR [#14822](https://github.com/fastapi/fastapi/pull/14822) by [@tiangolo](https://github.com/tiangolo).
* 🔨 Update docs and translations scripts, enable Turkish. PR [#14824](https://github.com/fastapi/fastapi/pull/14824) by [@tiangolo](https://github.com/tiangolo).

### Internal

* 🔨 Add max pages to translate to configs. PR [#14840](https://github.com/fastapi/fastapi/pull/14840) by [@tiangolo](https://github.com/tiangolo).

## 0.128.1 (2026-02-04)

### Features

* ✨ Add `viewport` meta tag to improve Swagger UI on mobile devices. PR [#14777](https://github.com/fastapi/fastapi/pull/14777) by [@Joab0](https://github.com/Joab0).
* 🚸 Improve error message for invalid query parameter type annotations. PR [#14479](https://github.com/fastapi/fastapi/pull/14479) by [@retwish](https://github.com/retwish).

### Fixes

* 🐛 Update `ValidationError` schema to include `input` and `ctx`. PR [#14791](https://github.com/fastapi/fastapi/pull/14791) by [@jonathan-fulton](https://github.com/jonathan-fulton).
* 🐛 Fix TYPE_CHECKING annotations for Python 3.14 (PEP 649). PR [#14789](https://github.com/fastapi/fastapi/pull/14789) by [@mgu](https://github.com/mgu).
* 🐛 Strip whitespaces from `Authorization` header credentials. PR [#14786](https://github.com/fastapi/fastapi/pull/14786) by [@WaveTheory1](https://github.com/WaveTheory1).
* 🐛 Fix OpenAPI duplication of `anyOf` refs for app-level responses with specified `content` and `model` as `Union`. PR [#14463](https://github.com/fastapi/fastapi/pull/14463) by [@DJMcoder](https://github.com/DJMcoder).

### Refactors

* 🎨 Tweak types for mypy. PR [#14816](https://github.com/fastapi/fastapi/pull/14816) by [@tiangolo](https://github.com/tiangolo).
* 🏷️ Re-export `IncEx` type from Pydantic instead of duplicating it. PR [#14641](https://github.com/fastapi/fastapi/pull/14641) by [@mvanderlee](https://github.com/mvanderlee).
* 💡 Update comment for Pydantic internals. PR [#14814](https://github.com/fastapi/fastapi/pull/14814) by [@tiangolo](https://github.com/tiangolo).

### Docs

* 📝 Update docs for contributing translations, simplify title. PR [#14817](https://github.com/fastapi/fastapi/pull/14817) by [@tiangolo](https://github.com/tiangolo).
* 📝 Fix typing issue in `docs_src/app_testing/app_b` code example. PR [#14573](https://github.com/fastapi/fastapi/pull/14573) by [@timakaa](https://github.com/timakaa).
* 📝 Fix example of license identifier in documentation. PR [#14492](https://github.com/fastapi/fastapi/pull/14492) by [@johnson-earls](https://github.com/johnson-earls).
* 📝 Add banner to translated pages. PR [#14809](https://github.com/fastapi/fastapi/pull/14809) by [@YuriiMotov](https://github.com/YuriiMotov).
* 📝 Add links to related sections of docs to docstrings. PR [#14776](https://github.com/fastapi/fastapi/pull/14776) by [@YuriiMotov](https://github.com/YuriiMotov).
* 📝 Update embedded code examples to Python 3.10 syntax. PR [#14758](https://github.com/fastapi/fastapi/pull/14758) by [@YuriiMotov](https://github.com/YuriiMotov).
* 📝 Fix dependency installation command in `docs/en/docs/contributing.md`. PR [#14757](https://github.com/fastapi/fastapi/pull/14757) by [@YuriiMotov](https://github.com/YuriiMotov).
* 📝 Use return type annotation instead of `response_model` when possible. PR [#14753](https://github.com/fastapi/fastapi/pull/14753) by [@YuriiMotov](https://github.com/YuriiMotov).
* 📝 Use `WSGIMiddleware` from `a2wsgi` instead of deprecated `fastapi.middleware.wsgi.WSGIMiddleware`. PR [#14756](https://github.com/fastapi/fastapi/pull/14756) by [@YuriiMotov](https://github.com/YuriiMotov).
* 📝 Fix minor typos in release notes. PR [#14780](https://github.com/fastapi/fastapi/pull/14780) by [@whyvineet](https://github.com/whyvineet).
* 🐛 Fix copy button in custom.js. PR [#14722](https://github.com/fastapi/fastapi/pull/14722) by [@fcharrier](https://github.com/fcharrier).
* 📝 Add contribution instructions about LLM generated code and comments and automated tools for PRs. PR [#14706](https://github.com/fastapi/fastapi/pull/14706) by [@tiangolo](https://github.com/tiangolo).
* 📝 Update docs for management tasks. PR [#14705](https://github.com/fastapi/fastapi/pull/14705) by [@tiangolo](https://github.com/tiangolo).
* 📝 Update docs about managing translations. PR [#14704](https://github.com/fastapi/fastapi/pull/14704) by [@tiangolo](https://github.com/tiangolo).
* 📝 Update docs for contributing with translations. PR [#14701](https://github.com/fastapi/fastapi/pull/14701) by [@tiangolo](https://github.com/tiangolo).
* 📝 Specify language code for code block. PR [#14656](https://github.com/fastapi/fastapi/pull/14656) by [@YuriiMotov](https://github.com/YuriiMotov).

### Translations

* 🌐 Improve LLM prompt of `uk` documentation. PR [#14795](https://github.com/fastapi/fastapi/pull/14795) by [@roli2py](https://github.com/roli2py).
* 🌐 Update translations for ja (update-outdated). PR [#14588](https://github.com/fastapi/fastapi/pull/14588) by [@tiangolo](https://github.com/tiangolo).
* 🌐 Update translations for uk (update outdated, found by fixer tool). PR [#14739](https://github.com/fastapi/fastapi/pull/14739) by [@YuriiMotov](https://github.com/YuriiMotov).
* 🌐 Update translations for tr (update-outdated). PR [#14745](https://github.com/fastapi/fastapi/pull/14745) by [@tiangolo](https://github.com/tiangolo).
* 🌐 Update `llm-prompt.md` for Korean language. PR [#14763](https://github.com/fastapi/fastapi/pull/14763) by [@seuthootDev](https://github.com/seuthootDev).
* 🌐 Update translations for ko (update outdated, found by fixer tool). PR [#14738](https://github.com/fastapi/fastapi/pull/14738) by [@YuriiMotov](https://github.com/YuriiMotov).
* 🌐 Update translations for de (update-outdated). PR [#14690](https://github.com/fastapi/fastapi/pull/14690) by [@tiangolo](https://github.com/tiangolo).
* 🌐 Update LLM prompt for Russian translations. PR [#14733](https://github.com/fastapi/fastapi/pull/14733) by [@YuriiMotov](https://github.com/YuriiMotov).
* 🌐 Update translations for ru (update-outdated). PR [#14693](https://github.com/fastapi/fastapi/pull/14693) by [@tiangolo](https://github.com/tiangolo).
* 🌐 Update translations for pt (update-outdated). PR [#14724](https://github.com/fastapi/fastapi/pull/14724) by [@tiangolo](https://github.com/tiangolo).
* 🌐 Update Korean LLM prompt. PR [#14740](https://github.com/fastapi/fastapi/pull/14740) by [@hard-coders](https://github.com/hard-coders).
* 🌐 Improve LLM prompt for Turkish translations. PR [#14728](https://github.com/fastapi/fastapi/pull/14728) by [@Kadermiyanyedi](https://github.com/Kadermiyanyedi).
* 🌐 Update portuguese llm-prompt.md. PR [#14702](https://github.com/fastapi/fastapi/pull/14702) by [@ceb10n](https://github.com/ceb10n).
* 🌐 Update LLM prompt instructions file for French. PR [#14618](https://github.com/fastapi/fastapi/pull/14618) by [@tiangolo](https://github.com/tiangolo).
* 🌐 Update translations for ko (add-missing). PR [#14699](https://github.com/fastapi/fastapi/pull/14699) by [@tiangolo](https://github.com/tiangolo).
* 🌐 Update translations for ko (update-outdated). PR [#14589](https://github.com/fastapi/fastapi/pull/14589) by [@tiangolo](https://github.com/tiangolo).
* 🌐 Update translations for uk (update-outdated). PR [#14587](https://github.com/fastapi/fastapi/pull/14587) by [@tiangolo](https://github.com/tiangolo).
* 🌐 Update translations for es (update-outdated). PR [#14686](https://github.com/fastapi/fastapi/pull/14686) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Add LLM prompt file for Turkish, generated from the existing translations. PR [#14547](https://github.com/fastapi/fastapi/pull/14547) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Add LLM prompt file for Traditional Chinese, generated from the existing translations. PR [#14550](https://github.com/fastapi/fastapi/pull/14550) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Add LLM prompt file for Simplified Chinese, generated from the existing translations. PR [#14549](https://github.com/fastapi/fastapi/pull/14549) by [@tiangolo](https://github.com/tiangolo).

### Internal

* ⬇️ Downgrade LLM translations model to GPT-5 to reduce mistakes. PR [#14823](https://github.com/fastapi/fastapi/pull/14823) by [@tiangolo](https://github.com/tiangolo).
* 🐛 Fix translation script commit in place. PR [#14818](https://github.com/fastapi/fastapi/pull/14818) by [@tiangolo](https://github.com/tiangolo).
* 🔨 Update translation script to retry if LLM-response doesn't pass validation with Translation Fixer tool. PR [#14749](https://github.com/fastapi/fastapi/pull/14749) by [@YuriiMotov](https://github.com/YuriiMotov).
* 👷 Run tests only on relevant code changes (not on docs). PR [#14813](https://github.com/fastapi/fastapi/pull/14813) by [@tiangolo](https://github.com/tiangolo).
* 👷 Run mypy by pre-commit. PR [#14806](https://github.com/fastapi/fastapi/pull/14806) by [@YuriiMotov](https://github.com/YuriiMotov).
* ⬆ Bump ruff from 0.14.3 to 0.14.14. PR [#14798](https://github.com/fastapi/fastapi/pull/14798) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump pyasn1 from 0.6.1 to 0.6.2. PR [#14804](https://github.com/fastapi/fastapi/pull/14804) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump sqlmodel from 0.0.27 to 0.0.31. PR [#14802](https://github.com/fastapi/fastapi/pull/14802) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump mkdocs-macros-plugin from 1.4.1 to 1.5.0. PR [#14801](https://github.com/fastapi/fastapi/pull/14801) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump gitpython from 3.1.45 to 3.1.46. PR [#14800](https://github.com/fastapi/fastapi/pull/14800) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump typer from 0.16.0 to 0.21.1. PR [#14799](https://github.com/fastapi/fastapi/pull/14799) by [@dependabot[bot]](https://github.com/apps/dependabot).
* 👥 Update FastAPI GitHub topic repositories. PR [#14803](https://github.com/fastapi/fastapi/pull/14803) by [@tiangolo](https://github.com/tiangolo).
* 👥 Update FastAPI People - Contributors and Translators. PR [#14796](https://github.com/fastapi/fastapi/pull/14796) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Ensure that an edit to `uv.lock` gets the `internal` label. PR [#14759](https://github.com/fastapi/fastapi/pull/14759) by [@svlandeg](https://github.com/svlandeg).
* 🔧 Update sponsors: remove Requestly. PR [#14735](https://github.com/fastapi/fastapi/pull/14735) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Update sponsors, LambdaTest changes to TestMu AI. PR [#14734](https://github.com/fastapi/fastapi/pull/14734) by [@tiangolo](https://github.com/tiangolo).
* ⬆ Bump actions/cache from 4 to 5. PR [#14511](https://github.com/fastapi/fastapi/pull/14511) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump actions/upload-artifact from 5 to 6. PR [#14525](https://github.com/fastapi/fastapi/pull/14525) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump actions/download-artifact from 6 to 7. PR [#14526](https://github.com/fastapi/fastapi/pull/14526) by [@dependabot[bot]](https://github.com/apps/dependabot).
* 👷 Tweak CI input names. PR [#14688](https://github.com/fastapi/fastapi/pull/14688) by [@tiangolo](https://github.com/tiangolo).
* 🔨 Refactor translation script to allow committing in place. PR [#14687](https://github.com/fastapi/fastapi/pull/14687) by [@tiangolo](https://github.com/tiangolo).
* 🐛 Fix translation script path. PR [#14685](https://github.com/fastapi/fastapi/pull/14685) by [@tiangolo](https://github.com/tiangolo).
* ✅ Enable tests in CI for scripts. PR [#14684](https://github.com/fastapi/fastapi/pull/14684) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Add pre-commit local script to fix language translations. PR [#14683](https://github.com/fastapi/fastapi/pull/14683) by [@tiangolo](https://github.com/tiangolo).
* ⬆️  Migrate to uv. PR [#14676](https://github.com/fastapi/fastapi/pull/14676) by [@DoctorJohn](https://github.com/DoctorJohn).
* 🔨 Add LLM translations tool fixer. PR [#14652](https://github.com/fastapi/fastapi/pull/14652) by [@YuriiMotov](https://github.com/YuriiMotov).
* 👥 Update FastAPI People - Sponsors. PR [#14626](https://github.com/fastapi/fastapi/pull/14626) by [@tiangolo](https://github.com/tiangolo).
* 👥 Update FastAPI GitHub topic repositories. PR [#14630](https://github.com/fastapi/fastapi/pull/14630) by [@tiangolo](https://github.com/tiangolo).
* 👥 Update FastAPI People - Contributors and Translators. PR [#14625](https://github.com/fastapi/fastapi/pull/14625) by [@tiangolo](https://github.com/tiangolo).
* 🌐 Update translation prompts. PR [#14619](https://github.com/fastapi/fastapi/pull/14619) by [@tiangolo](https://github.com/tiangolo).
* 🔨 Update LLM translation script to guide reviewers to change the prompt. PR [#14614](https://github.com/fastapi/fastapi/pull/14614) by [@tiangolo](https://github.com/tiangolo).
* 👷 Do not run translations on cron while finishing updating existing languages. PR [#14613](https://github.com/fastapi/fastapi/pull/14613) by [@tiangolo](https://github.com/tiangolo).
* 🔥 Remove test variants for Pydantic v1 in test_request_params. PR [#14612](https://github.com/fastapi/fastapi/pull/14612) by [@tiangolo](https://github.com/tiangolo).
* 🔥 Remove Pydantic v1  specific test variants. PR [#14611](https://github.com/fastapi/fastapi/pull/14611) by [@tiangolo](https://github.com/tiangolo).

## 0.128.0 (2025-12-27)

### Breaking Changes

* ➖ Drop support for `pydantic.v1`. PR [#14609](https://github.com/fastapi/fastapi/pull/14609) by [@tiangolo](https://github.com/tiangolo).

### Internal

* ✅ Run performance tests only on Pydantic v2. PR [#14608](https://github.com/fastapi/fastapi/pull/14608) by [@tiangolo](https://github.com/tiangolo).

## 0.127.1 (2025-12-26)

### Refactors

* 🔊 Add a custom `FastAPIDeprecationWarning`. PR [#14605](https://github.com/fastapi/fastapi/pull/14605) by [@tiangolo](https://github.com/tiangolo).

### Docs

* 📝 Add documentary to website. PR [#14600](https://github.com/fastapi/fastapi/pull/14600) by [@tiangolo](https://github.com/tiangolo).

### Translations

* 🌐 Update translations for de (update-outdated). PR [#14602](https://github.com/fastapi/fastapi/pull/14602) by [@nilslindemann](https://github.com/nilslindemann).
* 🌐 Update translations for de (update-outdated). PR [#14581](https://github.com/fastapi/fastapi/pull/14581) by [@nilslindemann](https://github.com/nilslindemann).

### Internal

* 🔧 Update pre-commit to use local Ruff instead of hook. PR [#14604](https://github.com/fastapi/fastapi/pull/14604) by [@tiangolo](https://github.com/tiangolo).
* ✅ Add missing tests for code examples. PR [#14569](https://github.com/fastapi/fastapi/pull/14569) by [@YuriiMotov](https://github.com/YuriiMotov).
* 👷 Remove `lint` job from `test` CI workflow. PR [#14593](https://github.com/fastapi/fastapi/pull/14593) by [@YuriiMotov](https://github.com/YuriiMotov).
* 👷 Update secrets check. PR [#14592](https://github.com/fastapi/fastapi/pull/14592) by [@tiangolo](https://github.com/tiangolo).
* 👷 Run CodSpeed tests in parallel to other tests to speed up CI. PR [#14586](https://github.com/fastapi/fastapi/pull/14586) by [@tiangolo](https://github.com/tiangolo).
* 🔨 Update scripts and pre-commit to autofix files. PR [#14585](https://github.com/fastapi/fastapi/pull/14585) by [@tiangolo](https://github.com/tiangolo).

## 0.127.0 (2025-12-21)

### Breaking Changes

* 🔊 Add deprecation warnings when using `pydantic.v1`. PR [#14583](https://github.com/fastapi/fastapi/pull/14583) by [@tiangolo](https://github.com/tiangolo).

### Translations

* 🔧 Add LLM prompt file for Korean, generated from the existing translations. PR [#14546](https://github.com/fastapi/fastapi/pull/14546) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Add LLM prompt file for Japanese, generated from the existing translations. PR [#14545](https://github.com/fastapi/fastapi/pull/14545) by [@tiangolo](https://github.com/tiangolo).

### Internal

* ⬆️ Upgrade OpenAI model for translations to gpt-5.2. PR [#14579](https://github.com/fastapi/fastapi/pull/14579) by [@tiangolo](https://github.com/tiangolo).

## 0.126.0 (2025-12-20)

### Upgrades

* ➖ Drop support for Pydantic v1, keeping short temporary support for Pydantic v2's `pydantic.v1`. PR [#14575](https://github.com/fastapi/fastapi/pull/14575) by [@tiangolo](https://github.com/tiangolo).
    * The minimum version of Pydantic installed is now `pydantic >=2.7.0`.
    * The `standard` dependencies now include `pydantic-settings >=2.0.0` and `pydantic-extra-types >=2.0.0`.

### Docs

* 📝 Fix duplicated variable in `docs_src/python_types/tutorial005_py39.py`. PR [#14565](https://github.com/fastapi/fastapi/pull/14565) by [@paras-verma7454](https://github.com/paras-verma7454).

### Translations

* 🔧 Add LLM prompt file for Ukrainian, generated from the existing translations. PR [#14548](https://github.com/fastapi/fastapi/pull/14548) by [@tiangolo](https://github.com/tiangolo).

### Internal

* 🔧 Tweak pre-commit to allow committing release-notes. PR [#14577](https://github.com/fastapi/fastapi/pull/14577) by [@tiangolo](https://github.com/tiangolo).
* ⬆️ Use prek as a pre-commit alternative. PR [#14572](https://github.com/fastapi/fastapi/pull/14572) by [@tiangolo](https://github.com/tiangolo).
* 👷 Add performance tests with CodSpeed. PR [#14558](https://github.com/fastapi/fastapi/pull/14558) by [@tiangolo](https://github.com/tiangolo).

## 0.125.0 (2025-12-17)

### Breaking Changes

* 🔧 Drop support for Python 3.8. PR [#14563](https://github.com/fastapi/fastapi/pull/14563) by [@tiangolo](https://github.com/tiangolo).
    * This would actually not be a _breaking_ change as no code would really break. Any Python 3.8 installer would just refuse to install the latest version of FastAPI and would only install 0.124.4. Only marking it as a "breaking change" to make it visible.

### Refactors

* ♻️ Upgrade internal syntax to Python 3.9+ 🎉. PR [#14564](https://github.com/fastapi/fastapi/pull/14564) by [@tiangolo](https://github.com/tiangolo).

### Docs

* ⚰️ Remove Python 3.8 from CI and remove Python 3.8 examples from source docs. PR [#14559](https://github.com/fastapi/fastapi/pull/14559) by [@YuriiMotov](https://github.com/YuriiMotov) and [@tiangolo](https://github.com/tiangolo).

### Translations

* 🌐 Update translations for pt (add-missing). PR [#14539](https://github.com/fastapi/fastapi/pull/14539) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Add LLM prompt file for French, generated from the existing French docs. PR [#14544](https://github.com/fastapi/fastapi/pull/14544) by [@tiangolo](https://github.com/tiangolo).
* 🌐 Sync Portuguese docs (pages found with script). PR [#14554](https://github.com/fastapi/fastapi/pull/14554) by [@YuriiMotov](https://github.com/YuriiMotov).
* 🌐 Sync Spanish docs (outdated pages found with script). PR [#14553](https://github.com/fastapi/fastapi/pull/14553) by [@YuriiMotov](https://github.com/YuriiMotov).
* 🌐 Sync German docs. PR [#14519](https://github.com/fastapi/fastapi/pull/14519) by [@nilslindemann](https://github.com/nilslindemann).
* 🔥 Remove inactive/scarce translations to Vietnamese. PR [#14543](https://github.com/fastapi/fastapi/pull/14543) by [@tiangolo](https://github.com/tiangolo).
* 🔥 Remove inactive/scarce translations to Persian. PR [#14542](https://github.com/fastapi/fastapi/pull/14542) by [@tiangolo](https://github.com/tiangolo).
* 🔥 Remove translation to emoji to simplify the new setup with LLM autotranslations. PR [#14541](https://github.com/fastapi/fastapi/pull/14541) by [@tiangolo](https://github.com/tiangolo).
* 🌐 Update translations for pt (update-outdated). PR [#14537](https://github.com/fastapi/fastapi/pull/14537) by [@tiangolo](https://github.com/tiangolo).
* 🌐 Update translations for es (update-outdated). PR [#14532](https://github.com/fastapi/fastapi/pull/14532) by [@tiangolo](https://github.com/tiangolo).
* 🌐 Update translations for es (add-missing). PR [#14533](https://github.com/fastapi/fastapi/pull/14533) by [@tiangolo](https://github.com/tiangolo).
* 🌐 Remove translations for removed docs. PR [#14516](https://github.com/fastapi/fastapi/pull/14516) by [@tiangolo](https://github.com/tiangolo).

### Internal

* ⬆ Bump `markdown-include-variants` from 0.0.7 to 0.0.8. PR [#14556](https://github.com/fastapi/fastapi/pull/14556) by [@YuriiMotov](https://github.com/YuriiMotov).
* 🔧 Temporarily disable translations still in progress, being migrated to the new LLM setup. PR [#14555](https://github.com/fastapi/fastapi/pull/14555) by [@YuriiMotov](https://github.com/YuriiMotov).
* 🔧 Update test workflow config, remove commented code. PR [#14540](https://github.com/fastapi/fastapi/pull/14540) by [@tiangolo](https://github.com/tiangolo).
* 👷 Configure coverage, error on main tests, don't wait for Smokeshow. PR [#14536](https://github.com/fastapi/fastapi/pull/14536) by [@tiangolo](https://github.com/tiangolo).
* 👷 Run Smokeshow always, even on test failures. PR [#14538](https://github.com/fastapi/fastapi/pull/14538) by [@tiangolo](https://github.com/tiangolo).
* 👷 Make Pydantic versions customizable in CI. PR [#14535](https://github.com/fastapi/fastapi/pull/14535) by [@tiangolo](https://github.com/tiangolo).
* 👷 Fix checkout GitHub Action fetch-depth for LLM translations, enable cron monthly. PR [#14531](https://github.com/fastapi/fastapi/pull/14531) by [@tiangolo](https://github.com/tiangolo).
* 👷 Fix Typer command for CI LLM translations. PR [#14530](https://github.com/fastapi/fastapi/pull/14530) by [@tiangolo](https://github.com/tiangolo).
* 👷 Update LLM translation CI, add language matrix and extra commands, prepare for scheduled run. PR [#14529](https://github.com/fastapi/fastapi/pull/14529) by [@tiangolo](https://github.com/tiangolo).
* 👷 Update github-actions user for GitHub Actions workflows. PR [#14528](https://github.com/fastapi/fastapi/pull/14528) by [@tiangolo](https://github.com/tiangolo).
* ➕ Add requirements for translations. PR [#14515](https://github.com/fastapi/fastapi/pull/14515) by [@tiangolo](https://github.com/tiangolo).

## 0.124.4 (2025-12-12)

### Fixes

* 🐛 Fix parameter aliases. PR [#14371](https://github.com/fastapi/fastapi/pull/14371) by [@YuriiMotov](https://github.com/YuriiMotov).

## 0.124.3 (2025-12-12)

### Fixes

* 🐛 Fix support for tagged union with discriminator inside of `Annotated` with `Body()`. PR [#14512](https://github.com/fastapi/fastapi/pull/14512) by [@tiangolo](https://github.com/tiangolo).

### Refactors

* ✅ Add set of tests for request parameters and alias. PR [#14358](https://github.com/fastapi/fastapi/pull/14358) by [@YuriiMotov](https://github.com/YuriiMotov).

### Docs

* 📝 Tweak links format. PR [#14505](https://github.com/fastapi/fastapi/pull/14505) by [@tiangolo](https://github.com/tiangolo).
* 📝 Update docs about re-raising validation errors, do not include string as is to not leak information. PR [#14487](https://github.com/fastapi/fastapi/pull/14487) by [@tiangolo](https://github.com/tiangolo).
* 🔥 Remove external links section. PR [#14486](https://github.com/fastapi/fastapi/pull/14486) by [@tiangolo](https://github.com/tiangolo).

### Translations

* 🌐 Sync Russian docs. PR [#14509](https://github.com/fastapi/fastapi/pull/14509) by [@YuriiMotov](https://github.com/YuriiMotov).
* 🌐 Sync German docs. PR [#14488](https://github.com/fastapi/fastapi/pull/14488) by [@nilslindemann](https://github.com/nilslindemann).

### Internal

* 👷 Tweak coverage to not pass Smokeshow max file size limit. PR [#14507](https://github.com/fastapi/fastapi/pull/14507) by [@tiangolo](https://github.com/tiangolo).
* ✅ Expand test matrix to include Windows and MacOS. PR [#14171](https://github.com/fastapi/fastapi/pull/14171) by [@svlandeg](https://github.com/svlandeg).

## 0.124.2 (2025-12-10)

### Fixes

* 🐛 Fix support for `if TYPE_CHECKING`,  non-evaluated stringified annotations. PR [#14485](https://github.com/fastapi/fastapi/pull/14485) by [@tiangolo](https://github.com/tiangolo).

## 0.124.1 (2025-12-10)

### Fixes

* 🐛 Fix handling arbitrary types when using `arbitrary_types_allowed=True`. PR [#14482](https://github.com/fastapi/fastapi/pull/14482) by [@tiangolo](https://github.com/tiangolo).

### Docs

* 📝 Add variants for code examples in "Advanced User Guide". PR [#14413](https://github.com/fastapi/fastapi/pull/14413) by [@YuriiMotov](https://github.com/YuriiMotov).
* 📝 Update tech stack in project generation docs. PR [#14472](https://github.com/fastapi/fastapi/pull/14472) by [@alejsdev](https://github.com/alejsdev).

### Internal

* ✅ Add test for Pydantic v2, dataclasses, UUID, and `__annotations__`. PR [#14477](https://github.com/fastapi/fastapi/pull/14477) by [@tiangolo](https://github.com/tiangolo).

## 0.124.0 (2025-12-06)

### Features

* 🚸  Improve tracebacks by adding endpoint metadata. PR [#14306](https://github.com/fastapi/fastapi/pull/14306) by [@savannahostrowski](https://github.com/savannahostrowski).

### Internal

* ✏️ Fix typo in `scripts/mkdocs_hooks.py`. PR [#14457](https://github.com/fastapi/fastapi/pull/14457) by [@yujiteshima](https://github.com/yujiteshima).

## 0.123.10 (2025-12-05)

### Fixes

* 🐛 Fix using class (not instance) dependency that has `__call__` method. PR [#14458](https://github.com/fastapi/fastapi/pull/14458) by [@YuriiMotov](https://github.com/YuriiMotov).
* 🐛 Fix `separate_input_output_schemas=False` with `computed_field`. PR [#14453](https://github.com/fastapi/fastapi/pull/14453) by [@YuriiMotov](https://github.com/YuriiMotov).

## 0.123.9 (2025-12-04)

### Fixes

* 🐛 Fix OAuth2 scopes in OpenAPI in extra corner cases, parent dependency with scopes, sub-dependency security scheme without scopes. PR [#14459](https://github.com/fastapi/fastapi/pull/14459) by [@tiangolo](https://github.com/tiangolo).

## 0.123.8 (2025-12-04)

### Fixes

* 🐛 Fix OpenAPI security scheme OAuth2 scopes declaration, deduplicate security schemes with different scopes. PR [#14455](https://github.com/fastapi/fastapi/pull/14455) by [@tiangolo](https://github.com/tiangolo).

## 0.123.7 (2025-12-04)

### Fixes

* 🐛 Fix evaluating stringified annotations in Python 3.10. PR [#11355](https://github.com/fastapi/fastapi/pull/11355) by [@chaen](https://github.com/chaen).

## 0.123.6 (2025-12-04)

### Fixes

* 🐛 Fix support for functools wraps and partial combined, for async and regular functions and classes in path operations and dependencies. PR [#14448](https://github.com/fastapi/fastapi/pull/14448) by [@tiangolo](https://github.com/tiangolo).

## 0.123.5 (2025-12-02)

### Features

* ✨ Allow using dependables with `functools.partial()`. PR [#9753](https://github.com/fastapi/fastapi/pull/9753) by [@lieryan](https://github.com/lieryan).
* ✨ Add support for wrapped functions (e.g. `@functools.wraps()`) used with forward references. PR [#5077](https://github.com/fastapi/fastapi/pull/5077) by [@lucaswiman](https://github.com/lucaswiman).
* ✨ Handle wrapped dependencies. PR [#9555](https://github.com/fastapi/fastapi/pull/9555) by [@phy1729](https://github.com/phy1729).

### Fixes

* 🐛 Fix optional sequence handling with new union syntax from Python 3.10. PR [#14430](https://github.com/fastapi/fastapi/pull/14430) by [@Viicos](https://github.com/Viicos).

### Refactors

* 🔥 Remove dangling extra conditional no longer needed. PR [#14435](https://github.com/fastapi/fastapi/pull/14435) by [@tiangolo](https://github.com/tiangolo).
* ♻️ Refactor internals, update `is_coroutine` check to reuse internal supported variants (unwrap, check class). PR [#14434](https://github.com/fastapi/fastapi/pull/14434) by [@tiangolo](https://github.com/tiangolo).

### Translations

* 🌐 Sync German docs. PR [#14367](https://github.com/fastapi/fastapi/pull/14367) by [@nilslindemann](https://github.com/nilslindemann).

## 0.123.4 (2025-12-02)

### Fixes

* 🐛 Fix OpenAPI schema support for computed fields when using `separate_input_output_schemas=False`. PR [#13207](https://github.com/fastapi/fastapi/pull/13207) by [@vgrafe](https://github.com/vgrafe).

### Docs

* 📝 Fix docstring of `servers` parameter. PR [#14405](https://github.com/fastapi/fastapi/pull/14405) by [@YuriiMotov](https://github.com/YuriiMotov).

## 0.123.3 (2025-12-02)

### Fixes

* 🐛 Fix Query\Header\Cookie parameter model alias. PR [#14360](https://github.com/fastapi/fastapi/pull/14360) by [@YuriiMotov](https://github.com/YuriiMotov).
* 🐛 Fix optional sequence handling in `serialize sequence value` with Pydantic V2. PR [#14297](https://github.com/fastapi/fastapi/pull/14297) by [@YuriiMotov](https://github.com/YuriiMotov).

## 0.123.2 (2025-12-02)

### Fixes

* 🐛 Fix unformatted `{type_}` in FastAPIError. PR [#14416](https://github.com/fastapi/fastapi/pull/14416) by [@Just-Helpful](https://github.com/Just-Helpful).
* 🐛 Fix parsing extra non-body parameter list. PR [#14356](https://github.com/fastapi/fastapi/pull/14356) by [@YuriiMotov](https://github.com/YuriiMotov).
* 🐛 Fix parsing extra `Form` parameter list. PR [#14303](https://github.com/fastapi/fastapi/pull/14303) by [@YuriiMotov](https://github.com/YuriiMotov).
* 🐛 Fix support for form values with empty strings interpreted as missing (`None` if that's the default), for compatibility with HTML forms. PR [#13537](https://github.com/fastapi/fastapi/pull/13537) by [@MarinPostma](https://github.com/MarinPostma).

### Docs

* 📝 Add tip on how to install `pip` in case of `No module named pip` error in `virtual-environments.md`. PR [#14211](https://github.com/fastapi/fastapi/pull/14211) by [@zadevhub](https://github.com/zadevhub).
* 📝 Update Primary Key notes for the SQL databases tutorial to avoid confusion. PR [#14120](https://github.com/fastapi/fastapi/pull/14120) by [@FlaviusRaducu](https://github.com/FlaviusRaducu).
* 📝 Clarify estimation note in documentation. PR [#14070](https://github.com/fastapi/fastapi/pull/14070) by [@SaisakthiM](https://github.com/SaisakthiM).

## 0.123.1 (2025-12-02)

### Fixes

* 🐛 Avoid accessing non-existing "$ref" key for Pydantic v2 compat remapping. PR [#14361](https://github.com/fastapi/fastapi/pull/14361) by [@svlandeg](https://github.com/svlandeg).
* 🐛 Fix `TypeError` when encoding a decimal with a `NaN` or `Infinity` value. PR [#12935](https://github.com/fastapi/fastapi/pull/12935) by [@kentwelcome](https://github.com/kentwelcome).

### Internal

* 🐛 Fix Windows UnicodeEncodeError in CLI test. PR [#14295](https://github.com/fastapi/fastapi/pull/14295) by [@hemanth-thirthahalli](https://github.com/hemanth-thirthahalli).
* 🔧 Update sponsors: add Greptile. PR [#14429](https://github.com/fastapi/fastapi/pull/14429) by [@tiangolo](https://github.com/tiangolo).
* 👥 Update FastAPI GitHub topic repositories. PR [#14426](https://github.com/fastapi/fastapi/pull/14426) by [@tiangolo](https://github.com/tiangolo).
* ⬆ Bump markdown-include-variants from 0.0.6 to 0.0.7. PR [#14423](https://github.com/fastapi/fastapi/pull/14423) by [@YuriiMotov](https://github.com/YuriiMotov).
* 👥 Update FastAPI People - Sponsors. PR [#14422](https://github.com/fastapi/fastapi/pull/14422) by [@tiangolo](https://github.com/tiangolo).
* 👥 Update FastAPI People - Contributors and Translators. PR [#14420](https://github.com/fastapi/fastapi/pull/14420) by [@tiangolo](https://github.com/tiangolo).

## 0.123.0 (2025-11-30)

### Fixes

* 🐛 Cache dependencies that don't use scopes and don't have sub-dependencies with scopes. PR [#14419](https://github.com/fastapi/fastapi/pull/14419) by [@tiangolo](https://github.com/tiangolo).

## 0.122.1 (2025-11-30)

### Fixes

* 🐛 Fix hierarchical security scope propagation. PR [#5624](https://github.com/fastapi/fastapi/pull/5624) by [@kristjanvalur](https://github.com/kristjanvalur).

### Docs

* 💅 Update CSS to explicitly use emoji font. PR [#14415](https://github.com/fastapi/fastapi/pull/14415) by [@tiangolo](https://github.com/tiangolo).

### Internal

* ⬆ Bump markdown-include-variants from 0.0.5 to 0.0.6. PR [#14418](https://github.com/fastapi/fastapi/pull/14418) by [@YuriiMotov](https://github.com/YuriiMotov).

## 0.122.0 (2025-11-24)

### Fixes

* 🐛 Use `401` status code in security classes when credentials are missing. PR [#13786](https://github.com/fastapi/fastapi/pull/13786) by [@YuriiMotov](https://github.com/YuriiMotov).
    * If your code depended on these classes raising the old (less correct) `403` status code, check the new docs about how to override the classes, to use the same old behavior: [Use Old 403 Authentication Error Status Codes](https://fastapi.tiangolo.com/how-to/authentication-error-status-code/).

### Internal

* 🔧 Configure labeler to exclude files that start from underscore for `lang-all` label. PR [#14213](https://github.com/fastapi/fastapi/pull/14213) by [@YuriiMotov](https://github.com/YuriiMotov).
* 👷 Add pre-commit config with local script for permalinks. PR [#14398](https://github.com/fastapi/fastapi/pull/14398) by [@tiangolo](https://github.com/tiangolo).
* 💄 Use font Fira Code to fix display of Rich panels in docs in Windows. PR [#14387](https://github.com/fastapi/fastapi/pull/14387) by [@tiangolo](https://github.com/tiangolo).
* 👷 Add custom pre-commit CI. PR [#14397](https://github.com/fastapi/fastapi/pull/14397) by [@tiangolo](https://github.com/tiangolo).
* ⬆ Bump actions/checkout from 5 to 6. PR [#14381](https://github.com/fastapi/fastapi/pull/14381) by [@dependabot[bot]](https://github.com/apps/dependabot).
* 👷 Upgrade `latest-changes` GitHub Action and pin `actions/checkout@v5`. PR [#14403](https://github.com/fastapi/fastapi/pull/14403) by [@svlandeg](https://github.com/svlandeg).
* 🛠️ Add `add-permalinks` and `add-permalinks-page` to `scripts/docs.py`. PR [#14033](https://github.com/fastapi/fastapi/pull/14033) by [@YuriiMotov](https://github.com/YuriiMotov).
* 🔧 Upgrade Material for MkDocs and remove insiders. PR [#14375](https://github.com/fastapi/fastapi/pull/14375) by [@tiangolo](https://github.com/tiangolo).

## 0.121.3 (2025-11-19)

### Refactors

* ♻️ Make the result of `Depends()` and `Security()` hashable, as a workaround for other tools interacting with these internal parts. PR [#14372](https://github.com/fastapi/fastapi/pull/14372) by [@tiangolo](https://github.com/tiangolo).

### Upgrades

* ⬆️ Bump Starlette to =0.23.0,=0.40.0,=0.23.0,=0.40.0,=0.40.0,=3.2.1,=0.0.18. PR [#13219](https://github.com/fastapi/fastapi/pull/13219) by [@DanielKusyDev](https://github.com/DanielKusyDev).
* ⬆️ Bump Starlette to allow up to 0.45.0: `>=0.40.0,=3.1.5. PR [#13194](https://github.com/fastapi/fastapi/pull/13194) by [@DanielKusyDev](https://github.com/DanielKusyDev).

### Refactors

* ✅ Simplify tests for websockets. PR [#13202](https://github.com/fastapi/fastapi/pull/13202) by [@alejsdev](https://github.com/alejsdev).
* ✅ Simplify tests for request_form_models . PR [#13183](https://github.com/fastapi/fastapi/pull/13183) by [@alejsdev](https://github.com/alejsdev).
* ✅ Simplify tests for separate_openapi_schemas. PR [#13201](https://github.com/fastapi/fastapi/pull/13201) by [@alejsdev](https://github.com/alejsdev).
* ✅ Simplify tests for security. PR [#13200](https://github.com/fastapi/fastapi/pull/13200) by [@alejsdev](https://github.com/alejsdev).
* ✅ Simplify tests for schema_extra_example. PR [#13197](https://github.com/fastapi/fastapi/pull/13197) by [@alejsdev](https://github.com/alejsdev).
* ✅ Simplify tests for request_model. PR [#13195](https://github.com/fastapi/fastapi/pull/13195) by [@alejsdev](https://github.com/alejsdev).
* ✅ Simplify tests for request_forms_and_files. PR [#13185](https://github.com/fastapi/fastapi/pull/13185) by [@alejsdev](https://github.com/alejsdev).
* ✅ Simplify tests for request_forms. PR [#13184](https://github.com/fastapi/fastapi/pull/13184) by [@alejsdev](https://github.com/alejsdev).
* ✅ Simplify tests for path_query_params. PR [#13181](https://github.com/fastapi/fastapi/pull/13181) by [@alejsdev](https://github.com/alejsdev).
* ✅ Simplify tests for path_operation_configurations. PR [#13180](https://github.com/fastapi/fastapi/pull/13180) by [@alejsdev](https://github.com/alejsdev).
* ✅ Simplify tests for header_params. PR [#13179](https://github.com/fastapi/fastapi/pull/13179) by [@alejsdev](https://github.com/alejsdev).
* ✅ Simplify tests for extra_models. PR [#13178](https://github.com/fastapi/fastapi/pull/13178) by [@alejsdev](https://github.com/alejsdev).
* ✅ Simplify tests for extra_data_types. PR [#13177](https://github.com/fastapi/fastapi/pull/13177) by [@alejsdev](https://github.com/alejsdev).
* ✅ Simplify tests for cookie_params. PR [#13176](https://github.com/fastapi/fastapi/pull/13176) by [@alejsdev](https://github.com/alejsdev).
* ✅ Simplify tests for dependencies. PR [#13174](https://github.com/fastapi/fastapi/pull/13174) by [@alejsdev](https://github.com/alejsdev).
* ✅ Simplify tests for body_updates. PR [#13172](https://github.com/fastapi/fastapi/pull/13172) by [@alejsdev](https://github.com/alejsdev).
* ✅ Simplify tests for body_nested_models. PR [#13171](https://github.com/fastapi/fastapi/pull/13171) by [@alejsdev](https://github.com/alejsdev).
* ✅ Simplify tests for body_multiple_params. PR [#13170](https://github.com/fastapi/fastapi/pull/13170) by [@alejsdev](https://github.com/alejsdev).
* ✅ Simplify tests for body_fields. PR [#13169](https://github.com/fastapi/fastapi/pull/13169) by [@alejsdev](https://github.com/alejsdev).
* ✅ Simplify tests for body. PR [#13168](https://github.com/fastapi/fastapi/pull/13168) by [@alejsdev](https://github.com/alejsdev).
* ✅ Simplify tests for bigger_applications. PR [#13167](https://github.com/fastapi/fastapi/pull/13167) by [@alejsdev](https://github.com/alejsdev).
* ✅ Simplify tests for background_tasks. PR [#13166](https://github.com/fastapi/fastapi/pull/13166) by [@alejsdev](https://github.com/alejsdev).
* ✅ Simplify tests for additional_status_codes. PR [#13149](https://github.com/fastapi/fastapi/pull/13149) by [@tiangolo](https://github.com/tiangolo).

### Docs

* ✏️ Update Strawberry integration docs. PR [#13155](https://github.com/fastapi/fastapi/pull/13155) by [@kinuax](https://github.com/kinuax).
* 🔥 Remove unused Peewee tutorial files. PR [#13158](https://github.com/fastapi/fastapi/pull/13158) by [@alejsdev](https://github.com/alejsdev).
* 📝 Update image in body-nested-model docs. PR [#11063](https://github.com/fastapi/fastapi/pull/11063) by [@untilhamza](https://github.com/untilhamza).
* 📝 Update `fastapi-cli` UI examples in docs. PR [#13107](https://github.com/fastapi/fastapi/pull/13107) by [@Zhongheng-Cheng](https://github.com/Zhongheng-Cheng).
* 👷 Add new GitHub Action to update contributors, translators, and translation reviewers. PR [#13136](https://github.com/fastapi/fastapi/pull/13136) by [@tiangolo](https://github.com/tiangolo).
* ✏️ Fix typo in `docs/en/docs/virtual-environments.md`. PR [#13124](https://github.com/fastapi/fastapi/pull/13124) by [@tiangolo](https://github.com/tiangolo).
* ✏️ Fix error in `docs/en/docs/contributing.md`. PR [#12899](https://github.com/fastapi/fastapi/pull/12899) by [@kingsubin](https://github.com/kingsubin).
* 📝 Minor corrections in `docs/en/docs/tutorial/sql-databases.md`. PR [#13081](https://github.com/fastapi/fastapi/pull/13081) by [@alv2017](https://github.com/alv2017).
* 📝 Update includes in `docs/ru/docs/tutorial/query-param-models.md`. PR [#12994](https://github.com/fastapi/fastapi/pull/12994) by [@alejsdev](https://github.com/alejsdev).
* ✏️ Fix typo in README installation instructions. PR [#13011](https://github.com/fastapi/fastapi/pull/13011) by [@dave-hay](https://github.com/dave-hay).
* 📝 Update docs for `fastapi-cli`. PR [#13031](https://github.com/fastapi/fastapi/pull/13031) by [@tiangolo](https://github.com/tiangolo).

### Translations

* 🌐 Update Portuguese Translation for `docs/pt/docs/tutorial/request-forms.md`. PR [#13216](https://github.com/fastapi/fastapi/pull/13216) by [@Joao-Pedro-P-Holanda](https://github.com/Joao-Pedro-P-Holanda).
* 🌐 Update Portuguese translation for `docs/pt/docs/advanced/settings.md`. PR [#13209](https://github.com/fastapi/fastapi/pull/13209) by [@ceb10n](https://github.com/ceb10n).
* 🌐 Add Portuguese translation for `docs/pt/docs/tutorial/security/oauth2-jwt.md`. PR [#13205](https://github.com/fastapi/fastapi/pull/13205) by [@ceb10n](https://github.com/ceb10n).
* 🌐 Add Indonesian translation for `docs/id/docs/index.md`. PR [#13191](https://github.com/fastapi/fastapi/pull/13191) by [@gerry-sabar](https://github.com/gerry-sabar).
* 🌐 Add Indonesian translation for `docs/id/docs/tutorial/static-files.md`. PR [#13092](https://github.com/fastapi/fastapi/pull/13092) by [@guspan-tanadi](https://github.com/guspan-tanadi).
* 🌐 Add Portuguese translation for `docs/pt/docs/tutorial/security/get-current-user.md`. PR [#13188](https://github.com/fastapi/fastapi/pull/13188) by [@ceb10n](https://github.com/ceb10n).
* 🌐 Remove Wrong Portuguese translations location for `docs/pt/docs/advanced/benchmarks.md`. PR [#13187](https://github.com/fastapi/fastapi/pull/13187) by [@ceb10n](https://github.com/ceb10n).
* 🌐 Update Portuguese translations. PR [#13156](https://github.com/fastapi/fastapi/pull/13156) by [@nillvitor](https://github.com/nillvitor).
* 🌐 Update Russian translation for `docs/ru/docs/tutorial/security/first-steps.md`. PR [#13159](https://github.com/fastapi/fastapi/pull/13159) by [@Yarous](https://github.com/Yarous).
* ✏️ Delete unnecessary backspace in `docs/ja/docs/tutorial/path-params-numeric-validations.md`. PR [#12238](https://github.com/fastapi/fastapi/pull/12238) by [@FakeDocument](https://github.com/FakeDocument).
* 🌐 Update Chinese translation for `docs/zh/docs/fastapi-cli.md`. PR [#13102](https://github.com/fastapi/fastapi/pull/13102) by [@Zhongheng-Cheng](https://github.com/Zhongheng-Cheng).
* 🌐 Add new Spanish translations for all docs with new LLM-assisted system using PydanticAI. PR [#13122](https://github.com/fastapi/fastapi/pull/13122) by [@tiangolo](https://github.com/tiangolo).
* 🌐 Update existing Spanish translations using the new LLM-assisted system using PydanticAI. PR [#13118](https://github.com/fastapi/fastapi/pull/13118) by [@tiangolo](https://github.com/tiangolo).
* 🌐 Update Chinese translation for `docs/zh/docs/advanced/security/oauth2-scopes.md`. PR [#13110](https://github.com/fastapi/fastapi/pull/13110) by [@ChenPu2002](https://github.com/ChenPu2002).
* 🌐 Add Indonesian translation for `docs/id/docs/tutorial/path-params.md`. PR [#13086](https://github.com/fastapi/fastapi/pull/13086) by [@gerry-sabar](https://github.com/gerry-sabar).
* 🌐 Add Korean translation for `docs/ko/docs/tutorial/sql-databases.md`. PR [#13093](https://github.com/fastapi/fastapi/pull/13093) by [@GeumBinLee](https://github.com/GeumBinLee).
* 🌐 Update Chinese translation for `docs/zh/docs/async.md`. PR [#13095](https://github.com/fastapi/fastapi/pull/13095) by [@Zhongheng-Cheng](https://github.com/Zhongheng-Cheng).
* 🌐 Add Chinese translation for `docs/zh/docs/advanced/openapi-webhooks.md`. PR [#13091](https://github.com/fastapi/fastapi/pull/13091) by [@Zhongheng-Cheng](https://github.com/Zhongheng-Cheng).
* 🌐 Add Chinese translation for `docs/zh/docs/advanced/async-tests.md`. PR [#13074](https://github.com/fastapi/fastapi/pull/13074) by [@Zhongheng-Cheng](https://github.com/Zhongheng-Cheng).
* 🌐 Add Ukrainian translation for `docs/uk/docs/fastapi-cli.md`. PR [#13020](https://github.com/fastapi/fastapi/pull/13020) by [@ykertytsky](https://github.com/ykertytsky).
* 🌐 Add Chinese translation for `docs/zh/docs/advanced/events.md`. PR [#12512](https://github.com/fastapi/fastapi/pull/12512) by [@ZhibangYue](https://github.com/ZhibangYue).
* 🌐 Add Russian translation for `/docs/ru/docs/tutorial/sql-databases.md`. PR [#13079](https://github.com/fastapi/fastapi/pull/13079) by [@alv2017](https://github.com/alv2017).
* 🌐 Update Chinese translation for `docs/zh/docs/advanced/testing-dependencies.md`. PR [#13066](https://github.com/fastapi/fastapi/pull/13066) by [@Zhongheng-Cheng](https://github.com/Zhongheng-Cheng).
* 🌐 Update Traditional Chinese translation for `docs/zh-hant/docs/tutorial/index.md`. PR [#13075](https://github.com/fastapi/fastapi/pull/13075) by [@codingjenny](https://github.com/codingjenny).
* 🌐 Add Chinese translation for `docs/zh/docs/tutorial/sql-databases.md`. PR [#13051](https://github.com/fastapi/fastapi/pull/13051) by [@Zhongheng-Cheng](https://github.com/Zhongheng-Cheng).
* 🌐 Update Chinese translation for `docs/zh/docs/tutorial/query-params-str-validations.md`. PR [#12928](https://github.com/fastapi/fastapi/pull/12928) by [@Vincy1230](https://github.com/Vincy1230).
* 🌐 Add Chinese translation for `docs/zh/docs/tutorial/header-param-models.md`. PR [#13040](https://github.com/fastapi/fastapi/pull/13040) by [@Zhongheng-Cheng](https://github.com/Zhongheng-Cheng).
* 🌐 Update Chinese translation for `docs/zh/docs/tutorial/path-params.md`. PR [#12926](https://github.com/fastapi/fastapi/pull/12926) by [@Vincy1230](https://github.com/Vincy1230).
* 🌐 Update Chinese translation for `docs/zh/docs/tutorial/first-steps.md`. PR [#12923](https://github.com/fastapi/fastapi/pull/12923) by [@Vincy1230](https://github.com/Vincy1230).
* 🌐 Update Russian translation for `docs/ru/docs/deployment/docker.md`. PR [#13048](https://github.com/fastapi/fastapi/pull/13048) by [@anklav24](https://github.com/anklav24).
* 🌐 Add Portuguese translation for `docs/pt/docs/advanced/generate-clients.md`. PR [#13030](https://github.com/fastapi/fastapi/pull/13030) by [@vitumenezes](https://github.com/vitumenezes).
* 🌐 Add Indonesian translation for `docs/id/docs/tutorial/first-steps.md`. PR [#13042](https://github.com/fastapi/fastapi/pull/13042) by [@gerry-sabar](https://github.com/gerry-sabar).
* 🌐 Add Chinese translation for `docs/zh/docs/tutorial/cookie-param-models.md`. PR [#13038](https://github.com/fastapi/fastapi/pull/13038) by [@Zhongheng-Cheng](https://github.com/Zhongheng-Cheng).
* 🌐 Add Chinese translation for `docs/zh/docs/tutorial/request-form-models.md`. PR [#13045](https://github.com/fastapi/fastapi/pull/13045) by [@Zhongheng-Cheng](https://github.com/Zhongheng-Cheng).
* 🌐 Add Russian translation for `docs/ru/docs/virtual-environments.md`. PR [#13026](https://github.com/fastapi/fastapi/pull/13026) by [@alv2017](https://github.com/alv2017).
* 🌐 Add Korean translation for `docs/ko/docs/tutorial/testing.md`. PR [#12968](https://github.com/fastapi/fastapi/pull/12968) by [@jts8257](https://github.com/jts8257).
* 🌐 Add Korean translation for `docs/ko/docs/advanced/async-test.md`. PR [#12918](https://github.com/fastapi/fastapi/pull/12918) by [@icehongssii](https://github.com/icehongssii).
* 🌐 Add Russian translation for `docs/ru/docs/tutorial/security/oauth2-jwt.md`. PR [#10601](https://github.com/fastapi/fastapi/pull/10601) by [@AlertRED](https://github.com/AlertRED).
* 🌐 Add Russian translation for `docs/ru/docs/tutorial/security/simple-oauth2.md`. PR [#10599](https://github.com/fastapi/fastapi/pull/10599) by [@AlertRED](https://github.com/AlertRED).
* 🌐 Add Russian translation for `docs/ru/docs/tutorial/security/get-current-user.md`. PR [#10594](https://github.com/fastapi/fastapi/pull/10594) by [@AlertRED](https://github.com/AlertRED).
* 🌐 Add Traditional Chinese translation for `docs/zh-hant/docs/features.md`. PR [#12441](https://github.com/fastapi/fastapi/pull/12441) by [@codingjenny](https://github.com/codingjenny).
* 🌐 Add Traditional Chinese translation for `docs/zh-hant/docs/virtual-environments.md`. PR [#12791](https://github.com/fastapi/fastapi/pull/12791) by [@Vincy1230](https://github.com/Vincy1230).
* 🌐 Add Korean translation for `docs/ko/docs/advanced/templates.md`. PR [#12726](https://github.com/fastapi/fastapi/pull/12726) by [@Heumhub](https://github.com/Heumhub).
* 🌐 Add Russian translation for `docs/ru/docs/fastapi-cli.md`. PR [#13041](https://github.com/fastapi/fastapi/pull/13041) by [@alv2017](https://github.com/alv2017).
* 🌐 Add Korean translation for `docs/ko/docs/tutorial/cookie-param-models.md`. PR [#13000](https://github.com/fastapi/fastapi/pull/13000) by [@hard-coders](https://github.com/hard-coders).
* 🌐 Add Korean translation for `docs/ko/docs/tutorial/header-param-models.md`. PR [#13001](https://github.com/fastapi/fastapi/pull/13001) by [@hard-coders](https://github.com/hard-coders).
* 🌐 Add Korean translation for `docs/ko/docs/tutorial/request-form-models.md`. PR [#13002](https://github.com/fastapi/fastapi/pull/13002) by [@hard-coders](https://github.com/hard-coders).
* 🌐 Add Korean translation for `docs/ko/docs/tutorial/request-forms.md`. PR [#13003](https://github.com/fastapi/fastapi/pull/13003) by [@hard-coders](https://github.com/hard-coders).
* 🌐 Add Korean translation for `docs/ko/docs/resources/index.md`. PR [#13004](https://github.com/fastapi/fastapi/pull/13004) by [@hard-coders](https://github.com/hard-coders).
* 🌐 Add Korean translation for `docs/ko/docs/how-to/configure-swagger-ui.md`. PR [#12898](https://github.com/fastapi/fastapi/pull/12898) by [@nahyunkeem](https://github.com/nahyunkeem).
* 🌐 Add Korean translation to `docs/ko/docs/advanced/additional-status-codes.md`. PR [#12715](https://github.com/fastapi/fastapi/pull/12715) by [@nahyunkeem](https://github.com/nahyunkeem).
* 🌐 Add Traditional Chinese translation for `docs/zh-hant/docs/tutorial/first-steps.md`. PR [#12467](https://github.com/fastapi/fastapi/pull/12467) by [@codingjenny](https://github.com/codingjenny).

### Internal

* 🔧 Add Pydantic 2 trove classifier. PR [#13199](https://github.com/fastapi/fastapi/pull/13199) by [@johnthagen](https://github.com/johnthagen).
* 👥 Update FastAPI People - Sponsors. PR [#13231](https://github.com/fastapi/fastapi/pull/13231) by [@tiangolo](https://github.com/tiangolo).
* 👷 Refactor FastAPI People Sponsors to use 2 tokens. PR [#13228](https://github.com/fastapi/fastapi/pull/13228) by [@tiangolo](https://github.com/tiangolo).
* 👷 Update token for FastAPI People - Sponsors. PR [#13225](https://github.com/fastapi/fastapi/pull/13225) by [@tiangolo](https://github.com/tiangolo).
* 👷 Add independent CI automation for FastAPI People - Sponsors. PR [#13221](https://github.com/fastapi/fastapi/pull/13221) by [@tiangolo](https://github.com/tiangolo).
* 👷 Add retries to Smokeshow. PR [#13151](https://github.com/fastapi/fastapi/pull/13151) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Update Speakeasy sponsor graphic. PR [#13147](https://github.com/fastapi/fastapi/pull/13147) by [@chailandau](https://github.com/chailandau).
* 👥 Update FastAPI GitHub topic repositories. PR [#13146](https://github.com/fastapi/fastapi/pull/13146) by [@tiangolo](https://github.com/tiangolo).
* 👷‍♀️ Add script for GitHub Topic Repositories and update External Links. PR [#13135](https://github.com/fastapi/fastapi/pull/13135) by [@alejsdev](https://github.com/alejsdev).
* 👥 Update FastAPI People - Contributors and Translators. PR [#13145](https://github.com/fastapi/fastapi/pull/13145) by [@tiangolo](https://github.com/tiangolo).
* ⬆ Bump markdown-include-variants from 0.0.3 to 0.0.4. PR [#13129](https://github.com/fastapi/fastapi/pull/13129) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump inline-snapshot from 0.14.0 to 0.18.1. PR [#13132](https://github.com/fastapi/fastapi/pull/13132) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump mkdocs-macros-plugin from 1.0.5 to 1.3.7. PR [#13133](https://github.com/fastapi/fastapi/pull/13133) by [@dependabot[bot]](https://github.com/apps/dependabot).
* 🔨 Add internal scripts to generate language translations with PydanticAI, include Spanish prompt. PR [#13123](https://github.com/fastapi/fastapi/pull/13123) by [@tiangolo](https://github.com/tiangolo).
* ⬆ Bump astral-sh/setup-uv from 4 to 5. PR [#13096](https://github.com/fastapi/fastapi/pull/13096) by [@dependabot[bot]](https://github.com/apps/dependabot).
* 🔧 Update sponsors: rename CryptAPI to BlockBee. PR [#13078](https://github.com/fastapi/fastapi/pull/13078) by [@tiangolo](https://github.com/tiangolo).
* ⬆ Bump pypa/gh-action-pypi-publish from 1.12.2 to 1.12.3. PR [#13055](https://github.com/fastapi/fastapi/pull/13055) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump types-ujson from 5.7.0.1 to 5.10.0.20240515. PR [#13018](https://github.com/fastapi/fastapi/pull/13018) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump black from 24.3.0 to 24.10.0. PR [#13014](https://github.com/fastapi/fastapi/pull/13014) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump inline-snapshot from 0.13.0 to 0.14.0. PR [#13017](https://github.com/fastapi/fastapi/pull/13017) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump dirty-equals from 0.6.0 to 0.8.0. PR [#13015](https://github.com/fastapi/fastapi/pull/13015) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump cloudflare/wrangler-action from 3.12 to 3.13. PR [#12996](https://github.com/fastapi/fastapi/pull/12996) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump astral-sh/setup-uv from 3 to 4. PR [#12982](https://github.com/fastapi/fastapi/pull/12982) by [@dependabot[bot]](https://github.com/apps/dependabot).
* 🔧 Remove duplicate actions/checkout in `notify-translations.yml`. PR [#12915](https://github.com/fastapi/fastapi/pull/12915) by [@tinyboxvk](https://github.com/tinyboxvk).
* 🔧 Update team members. PR [#13033](https://github.com/fastapi/fastapi/pull/13033) by [@tiangolo](https://github.com/tiangolo).
* 📝 Update sponsors: remove Codacy. PR [#13032](https://github.com/fastapi/fastapi/pull/13032) by [@tiangolo](https://github.com/tiangolo).

## 0.115.6 (2024-12-03)

### Fixes

* 🐛 Preserve traceback when an exception is raised in sync dependency with `yield`. PR [#5823](https://github.com/fastapi/fastapi/pull/5823) by [@sombek](https://github.com/sombek).

### Refactors

* ♻️ Update tests and internals for compatibility with Pydantic >=2.10. PR [#12971](https://github.com/fastapi/fastapi/pull/12971) by [@tamird](https://github.com/tamird).

### Docs

* 📝 Update includes format in docs with an automated script. PR [#12950](https://github.com/fastapi/fastapi/pull/12950) by [@tiangolo](https://github.com/tiangolo).
* 📝 Update includes for `docs/de/docs/advanced/using-request-directly.md`. PR [#12685](https://github.com/fastapi/fastapi/pull/12685) by [@alissadb](https://github.com/alissadb).
* 📝 Update includes for `docs/de/docs/how-to/conditional-openapi.md`. PR [#12689](https://github.com/fastapi/fastapi/pull/12689) by [@alissadb](https://github.com/alissadb).

### Translations

* 🌐 Add Traditional Chinese translation for `docs/zh-hant/docs/async.md`. PR [#12990](https://github.com/fastapi/fastapi/pull/12990) by [@ILoveSorasakiHina](https://github.com/ILoveSorasakiHina).
* 🌐 Add Traditional Chinese translation for `docs/zh-hant/docs/tutorial/query-param-models.md`. PR [#12932](https://github.com/fastapi/fastapi/pull/12932) by [@Vincy1230](https://github.com/Vincy1230).
* 🌐 Add Korean translation for `docs/ko/docs/advanced/testing-dependencies.md`. PR [#12992](https://github.com/fastapi/fastapi/pull/12992) by [@Limsunoh](https://github.com/Limsunoh).
* 🌐 Add Korean translation for `docs/ko/docs/advanced/websockets.md`. PR [#12991](https://github.com/fastapi/fastapi/pull/12991) by [@kwang1215](https://github.com/kwang1215).
* 🌐 Add Portuguese translation for `docs/pt/docs/tutorial/response-model.md`. PR [#12933](https://github.com/fastapi/fastapi/pull/12933) by [@AndreBBM](https://github.com/AndreBBM).
* 🌐 Add Korean translation for `docs/ko/docs/advanced/middlewares.md`. PR [#12753](https://github.com/fastapi/fastapi/pull/12753) by [@nahyunkeem](https://github.com/nahyunkeem).
* 🌐 Add Korean translation for `docs/ko/docs/advanced/openapi-webhooks.md`. PR [#12752](https://github.com/fastapi/fastapi/pull/12752) by [@saeye](https://github.com/saeye).
* 🌐 Add Chinese translation for `docs/zh/docs/tutorial/query-param-models.md`. PR [#12931](https://github.com/fastapi/fastapi/pull/12931) by [@Vincy1230](https://github.com/Vincy1230).
* 🌐 Add Russian translation for `docs/ru/docs/tutorial/query-param-models.md`. PR [#12445](https://github.com/fastapi/fastapi/pull/12445) by [@gitgernit](https://github.com/gitgernit).
* 🌐 Add Korean translation for `docs/ko/docs/tutorial/query-param-models.md`. PR [#12940](https://github.com/fastapi/fastapi/pull/12940) by [@jts8257](https://github.com/jts8257).
* 🔥 Remove obsolete tutorial translation to Chinese for `docs/zh/docs/tutorial/sql-databases.md`, it references files that are no longer on the repo. PR [#12949](https://github.com/fastapi/fastapi/pull/12949) by [@tiangolo](https://github.com/tiangolo).

### Internal

* ⬆ [pre-commit.ci] pre-commit autoupdate. PR [#12954](https://github.com/fastapi/fastapi/pull/12954) by [@pre-commit-ci[bot]](https://github.com/apps/pre-commit-ci).

## 0.115.5 (2024-11-12)

### Refactors

* ♻️ Update internal checks to support Pydantic 2.10. PR [#12914](https://github.com/fastapi/fastapi/pull/12914) by [@tiangolo](https://github.com/tiangolo).

### Docs

* 📝 Update includes for `docs/en/docs/tutorial/body.md`. PR [#12757](https://github.com/fastapi/fastapi/pull/12757) by [@gsheni](https://github.com/gsheni).
* 📝 Update includes in `docs/en/docs/advanced/testing-dependencies.md`. PR [#12647](https://github.com/fastapi/fastapi/pull/12647) by [@AyushSinghal1794](https://github.com/AyushSinghal1794).
* 📝 Update includes for `docs/en/docs/tutorial/metadata.md`. PR [#12773](https://github.com/fastapi/fastapi/pull/12773) by [@Nimitha-jagadeesha](https://github.com/Nimitha-jagadeesha).
* 📝 Update `docs/en/docs/tutorial/dependencies/dependencies-with-yield.md`. PR [#12045](https://github.com/fastapi/fastapi/pull/12045) by [@xuvjso](https://github.com/xuvjso).
* 📝 Update includes for `docs/en/docs/tutorial/dependencies/global-dependencies.md`. PR [#12653](https://github.com/fastapi/fastapi/pull/12653) by [@vishnuvskvkl](https://github.com/vishnuvskvkl).
* 📝 Update includes for `docs/en/docs/tutorial/body-updates.md`. PR [#12712](https://github.com/fastapi/fastapi/pull/12712) by [@davioc](https://github.com/davioc).
* 📝 Remove mention of Celery in the project generators. PR [#12742](https://github.com/fastapi/fastapi/pull/12742) by [@david-caro](https://github.com/david-caro).
* 📝 Update includes in `docs/en/docs/tutorial/header-param-models.md`. PR [#12814](https://github.com/fastapi/fastapi/pull/12814) by [@zhaohan-dong](https://github.com/zhaohan-dong).
* 📝 Update `contributing.md` docs, include note to not translate this page. PR [#12841](https://github.com/fastapi/fastapi/pull/12841) by [@tiangolo](https://github.com/tiangolo).
* 📝 Update includes in `docs/en/docs/tutorial/request-forms.md`. PR [#12648](https://github.com/fastapi/fastapi/pull/12648) by [@vishnuvskvkl](https://github.com/vishnuvskvkl).
* 📝 Update includes in `docs/en/docs/tutorial/request-form-models.md`. PR [#12649](https://github.com/fastapi/fastapi/pull/12649) by [@vishnuvskvkl](https://github.com/vishnuvskvkl).
* 📝 Update includes in `docs/en/docs/tutorial/security/oauth2-jwt.md`. PR [#12650](https://github.com/fastapi/fastapi/pull/12650) by [@OCE1960](https://github.com/OCE1960).
* 📝 Update includes in `docs/vi/docs/tutorial/first-steps.md`. PR [#12754](https://github.com/fastapi/fastapi/pull/12754) by [@MxPy](https://github.com/MxPy).
* 📝 Update includes for `docs/pt/docs/advanced/wsgi.md`. PR [#12769](https://github.com/fastapi/fastapi/pull/12769) by [@Nimitha-jagadeesha](https://github.com/Nimitha-jagadeesha).
* 📝 Update includes for `docs/en/docs/tutorial/dependencies/dependencies-in-path-operation-decorators.md`. PR [#12815](https://github.com/fastapi/fastapi/pull/12815) by [@handabaldeep](https://github.com/handabaldeep).
* 📝 Update includes for `docs/en/docs/tutorial/dependencies/classes-as-dependencies.md`. PR [#12813](https://github.com/fastapi/fastapi/pull/12813) by [@handabaldeep](https://github.com/handabaldeep).
* ✏️ Fix error in `docs/en/docs/tutorial/middleware.md`. PR [#12819](https://github.com/fastapi/fastapi/pull/12819) by [@alejsdev](https://github.com/alejsdev).
* 📝 Update includes for `docs/en/docs/tutorial/security/get-current-user.md`. PR [#12645](https://github.com/fastapi/fastapi/pull/12645) by [@OCE1960](https://github.com/OCE1960).
* 📝 Update includes for `docs/en/docs/tutorial/security/first-steps.md`. PR [#12643](https://github.com/fastapi/fastapi/pull/12643) by [@OCE1960](https://github.com/OCE1960).
* 📝 Update includes in `docs/de/docs/advanced/additional-responses.md`. PR [#12821](https://github.com/fastapi/fastapi/pull/12821) by [@zhaohan-dong](https://github.com/zhaohan-dong).
* 📝 Update includes in `docs/en/docs/advanced/generate-clients.md`. PR [#12642](https://github.com/fastapi/fastapi/pull/12642) by [@AyushSinghal1794](https://github.com/AyushSinghal1794).
* 📝 Fix admonition double quotes with new syntax. PR [#12835](https://github.com/fastapi/fastapi/pull/12835) by [@tiangolo](https://github.com/tiangolo).
* 📝 Update includes in `docs/zh/docs/advanced/additional-responses.md`. PR [#12828](https://github.com/fastapi/fastapi/pull/12828) by [@zhaohan-dong](https://github.com/zhaohan-dong).
* 📝 Update includes in `docs/en/docs/tutorial/path-params-numeric-validations.md`. PR [#12825](https://github.com/fastapi/fastapi/pull/12825) by [@zhaohan-dong](https://github.com/zhaohan-dong).
* 📝 Update includes for `docs/en/docs/advanced/testing-websockets.md`. PR [#12761](https://github.com/fastapi/fastapi/pull/12761) by [@hamidrasti](https://github.com/hamidrasti).
* 📝 Update includes for `docs/en/docs/advanced/using-request-directly.md`. PR [#12760](https://github.com/fastapi/fastapi/pull/12760) by [@hamidrasti](https://github.com/hamidrasti).
* 📝 Update includes for `docs/advanced/wsgi.md`. PR [#12758](https://github.com/fastapi/fastapi/pull/12758) by [@hamidrasti](https://github.com/hamidrasti).
* 📝 Update includes in `docs/de/docs/tutorial/middleware.md`. PR [#12729](https://github.com/fastapi/fastapi/pull/12729) by [@paintdog](https://github.com/paintdog).
* 📝 Update includes for `docs/en/docs/tutorial/schema-extra-example.md`. PR [#12822](https://github.com/fastapi/fastapi/pull/12822) by [@tiangolo](https://github.com/tiangolo).
* 📝 Update includes in `docs/fr/docs/advanced/additional-responses.md`. PR [#12634](https://github.com/fastapi/fastapi/pull/12634) by [@fegmorte](https://github.com/fegmorte).
* 📝 Update includes in `docs/fr/docs/advanced/path-operation-advanced-configuration.md`. PR [#12633](https://github.com/fastapi/fastapi/pull/12633) by [@kantandane](https://github.com/kantandane).
* 📝 Update includes in `docs/fr/docs/advanced/response-directly.md`. PR [#12632](https://github.com/fastapi/fastapi/pull/12632) by [@kantandane](https://github.com/kantandane).
* 📝 Update includes for `docs/en/docs/tutorial/header-params.md`. PR [#12640](https://github.com/fastapi/fastapi/pull/12640) by [@vishnuvskvkl](https://github.com/vishnuvskvkl).
* 📝 Update includes in `docs/en/docs/tutorial/cookie-param-models.md`. PR [#12639](https://github.com/fastapi/fastapi/pull/12639) by [@vishnuvskvkl](https://github.com/vishnuvskvkl).
* 📝 Update includes for `docs/en/docs/tutorial/extra-models.md`. PR [#12638](https://github.com/fastapi/fastapi/pull/12638) by [@vishnuvskvkl](https://github.com/vishnuvskvkl).
* 📝 Update includes for `docs/en/docs/tutorial/cors.md`. PR [#12637](https://github.com/fastapi/fastapi/pull/12637) by [@vishnuvskvkl](https://github.com/vishnuvskvkl).
* 📝 Update includes for `docs/en/docs/tutorial/dependencies/sub-dependencies.md`. PR [#12810](https://github.com/fastapi/fastapi/pull/12810) by [@handabaldeep](https://github.com/handabaldeep).
* 📝 Update includes in `docs/en/docs/tutorial/body-nested-models.md`. PR [#12812](https://github.com/fastapi/fastapi/pull/12812) by [@zhaohan-dong](https://github.com/zhaohan-dong).
* 📝 Update includes in `docs/en/docs/tutorial/path-operation-configuration.md`. PR [#12809](https://github.com/fastapi/fastapi/pull/12809) by [@AlexWendland](https://github.com/AlexWendland).
* 📝 Update includes in `docs/en/docs/tutorial/request-files.md`. PR [#12818](https://github.com/fastapi/fastapi/pull/12818) by [@zhaohan-dong](https://github.com/zhaohan-dong).
* 📝 Update includes for `docs/en/docs/tutorial/query-param-models.md`. PR [#12817](https://github.com/fastapi/fastapi/pull/12817) by [@handabaldeep](https://github.com/handabaldeep).
* 📝 Update includes in `docs/en/docs/tutorial/path-params.md`. PR [#12811](https://github.com/fastapi/fastapi/pull/12811) by [@AlexWendland](https://github.com/AlexWendland).
* 📝 Update includes in `docs/en/docs/tutorial/response-model.md`. PR [#12621](https://github.com/fastapi/fastapi/pull/12621) by [@kantandane](https://github.com/kantandane).
* 📝 Update includes in `docs/en/docs/advanced/websockets.md`. PR [#12606](https://github.com/fastapi/fastapi/pull/12606) by [@vishnuvskvkl](https://github.com/vishnuvskvkl).
* 📝 Updates include for `docs/en/docs/tutorial/cookie-params.md`. PR [#12808](https://github.com/fastapi/fastapi/pull/12808) by [@handabaldeep](https://github.com/handabaldeep).
* 📝 Update includes in `docs/en/docs/tutorial/middleware.md`. PR [#12807](https://github.com/fastapi/fastapi/pull/12807) by [@AlexWendland](https://github.com/AlexWendland).
* 📝 Update includes in `docs/en/docs/advanced/sub-applications.md`. PR [#12806](https://github.com/fastapi/fastapi/pull/12806) by [@zhaohan-dong](https://github.com/zhaohan-dong).
* 📝 Update includes in `docs/en/docs/advanced/response-headers.md`. PR [#12805](https://github.com/fastapi/fastapi/pull/12805) by [@zhaohan-dong](https://github.com/zhaohan-dong).
* 📝 Update includes in `docs/fr/docs/tutorial/first-steps.md`. PR [#12594](https://github.com/fastapi/fastapi/pull/12594) by [@kantandane](https://github.com/kantandane).
* 📝 Update includes in `docs/en/docs/advanced/response-cookies.md`. PR [#12804](https://github.com/fastapi/fastapi/pull/12804) by [@zhaohan-dong](https://github.com/zhaohan-dong).
* 📝 Update includes in `docs/en/docs/advanced/path-operation-advanced-configuration.md`. PR [#12802](https://github.com/fastapi/fastapi/pull/12802) by [@zhaohan-dong](https://github.com/zhaohan-dong).
* 📝 Update includes for `docs/en/docs/advanced/response-directly.md`. PR [#12803](https://github.com/fastapi/fastapi/pull/12803) by [@handabaldeep](https://github.com/handabaldeep).
* 📝 Update includes in `docs/zh/docs/tutorial/background-tasks.md`. PR [#12798](https://github.com/fastapi/fastapi/pull/12798) by [@zhaohan-dong](https://github.com/zhaohan-dong).
* 📝 Update includes for `docs/de/docs/tutorial/body-multiple-params.md`. PR [#12699](https://github.com/fastapi/fastapi/pull/12699) by [@alissadb](https://github.com/alissadb).
* 📝 Update includes in `docs/em/docs/tutorial/body-updates.md`. PR [#12799](https://github.com/fastapi/fastapi/pull/12799) by [@AlexWendland](https://github.com/AlexWendland).
* 📝 Update includes `docs/en/docs/advanced/response-change-status-code.md`. PR [#12801](https://github.com/fastapi/fastapi/pull/12801) by [@handabaldeep](https://github.com/handabaldeep).
* 📝 Update includes `docs/en/docs/advanced/openapi-callbacks.md`. PR [#12800](https://github.com/fastapi/fastapi/pull/12800) by [@handabaldeep](https://github.com/handabaldeep).
* 📝  Update includes in `docs/fr/docs/tutorial/body-multiple-params.md`. PR [#12598](https://github.com/fastapi/fastapi/pull/12598) by [@kantandane](https://github.com/kantandane).
* 📝 Update includes in `docs/en/docs/tutorial/body-multiple-params.md`. PR [#12593](https://github.com/fastapi/fastapi/pull/12593) by [@Tashanam-Shahbaz](https://github.com/Tashanam-Shahbaz).
* 📝 Update includes in `docs/pt/docs/tutorial/background-tasks.md`. PR [#12736](https://github.com/fastapi/fastapi/pull/12736) by [@bhunao](https://github.com/bhunao).
* 📝 Update includes for `docs/en/docs/advanced/custom-response.md`. PR [#12797](https://github.com/fastapi/fastapi/pull/12797) by [@handabaldeep](https://github.com/handabaldeep).
* 📝 Update includes for `docs/pt/docs/python-types.md`. PR [#12671](https://github.com/fastapi/fastapi/pull/12671) by [@ceb10n](https://github.com/ceb10n).
* 📝 Update includes for `docs/de/docs/python-types.md`. PR [#12660](https://github.com/fastapi/fastapi/pull/12660) by [@alissadb](https://github.com/alissadb).
* 📝 Update includes for `docs/de/docs/advanced/dataclasses.md`. PR [#12658](https://github.com/fastapi/fastapi/pull/12658) by [@alissadb](https://github.com/alissadb).
* 📝 Update includes in `docs/fr/docs/tutorial/path-params.md`. PR [#12592](https://github.com/fastapi/fastapi/pull/12592) by [@kantandane](https://github.com/kantandane).
* 📝 Update includes for `docs/de/docs/how-to/configure-swagger-ui.md`. PR [#12690](https://github.com/fastapi/fastapi/pull/12690) by [@alissadb](https://github.com/alissadb).
* 📝 Update includes in `docs/en/docs/advanced/security/oauth2-scopes.md`. PR [#12572](https://github.com/fastapi/fastapi/pull/12572) by [@krishnamadhavan](https://github.com/krishnamadhavan).
* 📝 Update includes for `docs/en/docs/how-to/conditional-openapi.md`. PR [#12624](https://github.com/fastapi/fastapi/pull/12624) by [@rabinlamadong](https://github.com/rabinlamadong).
* 📝 Update includes in `docs/en/docs/tutorial/dependencies/index.md`. PR [#12615](https://github.com/fastapi/fastapi/pull/12615) by [@bharara](https://github.com/bharara).
* 📝 Update includes in `docs/en/docs/tutorial/response-status-code.md`. PR [#12620](https://github.com/fastapi/fastapi/pull/12620) by [@kantandane](https://github.com/kantandane).
* 📝 Update includes in `docs/en/docs/how-to/custom-docs-ui-assets.md`. PR [#12623](https://github.com/fastapi/fastapi/pull/12623) by [@rabinlamadong](https://github.com/rabinlamadong).
* 📝 Update includes in `docs/en/docs/advanced/openapi-webhooks.md`. PR [#12605](https://github.com/fastapi/fastapi/pull/12605) by [@salmantec](https://github.com/salmantec).
* 📝 Update includes in `docs/en/docs/advanced/events.md`. PR [#12604](https://github.com/fastapi/fastapi/pull/12604) by [@salmantec](https://github.com/salmantec).
* 📝 Update includes in `docs/en/docs/advanced/dataclasses.md`. PR [#12603](https://github.com/fastapi/fastapi/pull/12603) by [@salmantec](https://github.com/salmantec).
* 📝 Update includes in `docs/es/docs/tutorial/cookie-params.md`. PR [#12602](https://github.com/fastapi/fastapi/pull/12602) by [@antonyare93](https://github.com/antonyare93).
* 📝 Update includes in `docs/fr/docs/tutorial/path-params-numeric-validations.md`. PR [#12601](https://github.com/fastapi/fastapi/pull/12601) by [@kantandane](https://github.com/kantandane).
* 📝 Update includes in `docs/fr/docs/tutorial/background-tasks.md`. PR [#12600](https://github.com/fastapi/fastapi/pull/12600) by [@kantandane](https://github.com/kantandane).
* 📝 Update includes in `docs/en/docs/tutorial/encoder.md`. PR [#12597](https://github.com/fastapi/fastapi/pull/12597) by [@tonyjly](https://github.com/tonyjly).
* 📝 Update includes in `docs/en/docs/how-to/custom-docs-ui-assets.md`. PR [#12557](https://github.com/fastapi/fastapi/pull/12557) by [@philipokiokio](https://github.com/philipokiokio).
* 🎨 Adjust spacing. PR [#12635](https://github.com/fastapi/fastapi/pull/12635) by [@alejsdev](https://github.com/alejsdev).
* 📝 Update includes in `docs/en/docs/how-to/custom-request-and-route.md`. PR [#12560](https://github.com/fastapi/fastapi/pull/12560) by [@philipokiokio](https://github.com/philipokiokio).

### Translations

* 🌐 Add Korean translation for `docs/ko/docs/advanced/testing-websockets.md`. PR [#12739](https://github.com/fastapi/fastapi/pull/12739) by [@Limsunoh](https://github.com/Limsunoh).
* 🌐 Add Traditional Chinese translation for `docs/zh-hant/docs/environment-variables.md`. PR [#12785](https://github.com/fastapi/fastapi/pull/12785) by [@Vincy1230](https://github.com/Vincy1230).
* 🌐 Add Chinese translation for `docs/zh/docs/environment-variables.md`. PR [#12784](https://github.com/fastapi/fastapi/pull/12784) by [@Vincy1230](https://github.com/Vincy1230).
* 🌐 Add Korean translation for `ko/docs/advanced/response-headers.md`. PR [#12740](https://github.com/fastapi/fastapi/pull/12740) by [@kwang1215](https://github.com/kwang1215).
* 🌐 Add Chinese translation for `docs/zh/docs/virtual-environments.md`. PR [#12790](https://github.com/fastapi/fastapi/pull/12790) by [@Vincy1230](https://github.com/Vincy1230).
* 🌐 Add Korean translation for `/docs/ko/docs/environment-variables.md`. PR [#12526](https://github.com/fastapi/fastapi/pull/12526) by [@Tolerblanc](https://github.com/Tolerblanc).
* 🌐 Add Korean translation for `docs/ko/docs/history-design-future.md`. PR [#12646](https://github.com/fastapi/fastapi/pull/12646) by [@saeye](https://github.com/saeye).
* 🌐 Add Korean translation for `docs/ko/docs/advanced/advanced-dependencies.md`. PR [#12675](https://github.com/fastapi/fastapi/pull/12675) by [@kim-sangah](https://github.com/kim-sangah).
* 🌐 Add Korean translation for `docs/ko/docs/how-to/conditional-openapi.md`. PR [#12731](https://github.com/fastapi/fastapi/pull/12731) by [@sptcnl](https://github.com/sptcnl).
* 🌐 Add Korean translation for `docs/ko/docs/advanced/using_request_directly.md`. PR [#12738](https://github.com/fastapi/fastapi/pull/12738) by [@kwang1215](https://github.com/kwang1215).
* 🌐 Add Korean translation for `docs/ko/docs/advanced/testing-events.md`. PR [#12741](https://github.com/fastapi/fastapi/pull/12741) by [@9zimin9](https://github.com/9zimin9).
* 🌐 Add Korean translation for `docs/ko/docs/security/index.md`. PR [#12743](https://github.com/fastapi/fastapi/pull/12743) by [@kim-sangah](https://github.com/kim-sangah).
* 🌐 Add Portuguese translation for `docs/pt/docs/advanced/path-operation-advanced-configuration.md`. PR [#12762](https://github.com/fastapi/fastapi/pull/12762) by [@Joao-Pedro-P-Holanda](https://github.com/Joao-Pedro-P-Holanda).
* 🌐 Add Korean translation for `docs/ko/docs/advanced/wsgi.md`. PR [#12659](https://github.com/fastapi/fastapi/pull/12659) by [@Limsunoh](https://github.com/Limsunoh).
* 🌐 Add Portuguese translation for `docs/pt/docs/advanced/websockets.md`. PR [#12703](https://github.com/fastapi/fastapi/pull/12703) by [@devfernandoa](https://github.com/devfernandoa).
* 🌐 Add Portuguese translation for `docs/pt/docs/tutorial/security/simple-oauth2.md`. PR [#12520](https://github.com/fastapi/fastapi/pull/12520) by [@LidiaDomingos](https://github.com/LidiaDomingos).
* 🌐 Add Korean translation for `docs/ko/docs/advanced/response-directly.md`. PR [#12674](https://github.com/fastapi/fastapi/pull/12674) by [@9zimin9](https://github.com/9zimin9).
* 🌐 Add Portuguese translation for `docs/pt/docs/advanced/middleware.md`. PR [#12704](https://github.com/fastapi/fastapi/pull/12704) by [@devluisrodrigues](https://github.com/devluisrodrigues).
* 🌐 Add Portuguese translation for `docs/pt/docs/advanced/openapi-callbacks.md`. PR [#12705](https://github.com/fastapi/fastapi/pull/12705) by [@devfernandoa](https://github.com/devfernandoa).
* 🌐 Add Portuguese translation for `docs/pt/docs/tutorial/request-files.md`. PR [#12706](https://github.com/fastapi/fastapi/pull/12706) by [@devluisrodrigues](https://github.com/devluisrodrigues).
* 🌐 Add Portuguese Translation for `docs/pt/docs/advanced/custom-response.md`. PR [#12631](https://github.com/fastapi/fastapi/pull/12631) by [@Joao-Pedro-P-Holanda](https://github.com/Joao-Pedro-P-Holanda).
* 🌐 Add Portuguese translation for `docs/pt/docs/tutorial/metadata.md`. PR [#12538](https://github.com/fastapi/fastapi/pull/12538) by [@LinkolnR](https://github.com/LinkolnR).
* 🌐 Add Korean translation for `docs/ko/docs/tutorial/metadata.md`. PR [#12541](https://github.com/fastapi/fastapi/pull/12541) by [@kwang1215](https://github.com/kwang1215).
* 🌐 Add Korean Translation for `docs/ko/docs/advanced/response-cookies.md`. PR [#12546](https://github.com/fastapi/fastapi/pull/12546) by [@kim-sangah](https://github.com/kim-sangah).
* 🌐 Add Korean translation for `docs/ko/docs/fastapi-cli.md`. PR [#12515](https://github.com/fastapi/fastapi/pull/12515) by [@dhdld](https://github.com/dhdld).
* 🌐 Add Korean Translation for `docs/ko/docs/advanced/response-change-status-code.md`. PR [#12547](https://github.com/fastapi/fastapi/pull/12547) by [@9zimin9](https://github.com/9zimin9).

### Internal

* ⬆ [pre-commit.ci] pre-commit autoupdate. PR [#12907](https://github.com/fastapi/fastapi/pull/12907) by [@pre-commit-ci[bot]](https://github.com/apps/pre-commit-ci).
* 🔨 Update docs preview script to show previous version and English version. PR [#12856](https://github.com/fastapi/fastapi/pull/12856) by [@tiangolo](https://github.com/tiangolo).
* ⬆ Bump tiangolo/latest-changes from 0.3.1 to 0.3.2. PR [#12794](https://github.com/fastapi/fastapi/pull/12794) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump pypa/gh-action-pypi-publish from 1.12.0 to 1.12.2. PR [#12788](https://github.com/fastapi/fastapi/pull/12788) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump pypa/gh-action-pypi-publish from 1.11.0 to 1.12.0. PR [#12781](https://github.com/fastapi/fastapi/pull/12781) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump cloudflare/wrangler-action from 3.11 to 3.12. PR [#12777](https://github.com/fastapi/fastapi/pull/12777) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ [pre-commit.ci] pre-commit autoupdate. PR [#12766](https://github.com/fastapi/fastapi/pull/12766) by [@pre-commit-ci[bot]](https://github.com/apps/pre-commit-ci).
* ⬆ Bump pypa/gh-action-pypi-publish from 1.10.3 to 1.11.0. PR [#12721](https://github.com/fastapi/fastapi/pull/12721) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Update pre-commit requirement from =2.17.0 to >=2.17.0,=1.1.2 to >=1.1.2,=7.1.3 to >=7.1.3,=0.40.0,=0.23.0 to >=0.23.0,=0.37.2,=1.3.18 to >=1.3.18,=0.37.2,=0.0.5`.

#### Technical Details

Before this, `fastapi` would include the standard dependencies, with Uvicorn and the `fastapi-cli`, etc.

And `fastapi-slim` would not include those standard dependencies.

Now `fastapi` doesn't include those standard dependencies unless you install with `pip install "fastapi[standard]"`.

Before, you would install `pip install fastapi`, now you should include the `standard` optional dependencies (unless you want to exclude one of those): `pip install "fastapi[standard]"`.

This change is because having the standard optional dependencies installed by default was being inconvenient to several users, and having to install instead `fastapi-slim` was not being a feasible solution.

Discussed here: [#11522](https://github.com/fastapi/fastapi/pull/11522) and here: [#11525](https://github.com/fastapi/fastapi/discussions/11525)

### Docs

* ✏️ Fix typos in docs. PR [#11926](https://github.com/fastapi/fastapi/pull/11926) by [@jianghuyiyuan](https://github.com/jianghuyiyuan).
* 📝 Tweak management docs. PR [#11918](https://github.com/fastapi/fastapi/pull/11918) by [@tiangolo](https://github.com/tiangolo).
* 🚚 Rename GitHub links from tiangolo/fastapi to fastapi/fastapi. PR [#11913](https://github.com/fastapi/fastapi/pull/11913) by [@tiangolo](https://github.com/tiangolo).
* 📝 Add docs about FastAPI team and project management. PR [#11908](https://github.com/tiangolo/fastapi/pull/11908) by [@tiangolo](https://github.com/tiangolo).
* 📝 Re-structure docs main menu. PR [#11904](https://github.com/tiangolo/fastapi/pull/11904) by [@tiangolo](https://github.com/tiangolo).
* 📝 Update Speakeasy URL. PR [#11871](https://github.com/tiangolo/fastapi/pull/11871) by [@ndimares](https://github.com/ndimares).

### Translations

* 🌐 Update Portuguese translation for `docs/pt/docs/alternatives.md`. PR [#11931](https://github.com/fastapi/fastapi/pull/11931) by [@ceb10n](https://github.com/ceb10n).
* 🌐 Add Russian translation for `docs/ru/docs/tutorial/dependencies/sub-dependencies.md`. PR [#10515](https://github.com/tiangolo/fastapi/pull/10515) by [@AlertRED](https://github.com/AlertRED).
* 🌐 Add Portuguese translation for `docs/pt/docs/advanced/response-change-status-code.md`. PR [#11863](https://github.com/tiangolo/fastapi/pull/11863) by [@ceb10n](https://github.com/ceb10n).
* 🌐 Add Portuguese translation for `docs/pt/docs/reference/background.md`. PR [#11849](https://github.com/tiangolo/fastapi/pull/11849) by [@lucasbalieiro](https://github.com/lucasbalieiro).
* 🌐 Add Portuguese translation for `docs/pt/docs/tutorial/dependencies/dependencies-with-yield.md`. PR [#11848](https://github.com/tiangolo/fastapi/pull/11848) by [@Joao-Pedro-P-Holanda](https://github.com/Joao-Pedro-P-Holanda).
* 🌐 Add Portuguese translation for `docs/pt/docs/reference/apirouter.md`. PR [#11843](https://github.com/tiangolo/fastapi/pull/11843) by [@lucasbalieiro](https://github.com/lucasbalieiro).

### Internal

* 🔧 Update sponsors: add liblab. PR [#11934](https://github.com/fastapi/fastapi/pull/11934) by [@tiangolo](https://github.com/tiangolo).
* 👷 Update GitHub Action label-approved permissions. PR [#11933](https://github.com/fastapi/fastapi/pull/11933) by [@tiangolo](https://github.com/tiangolo).
* 👷 Refactor GitHub Action to comment docs deployment URLs and update token. PR [#11925](https://github.com/fastapi/fastapi/pull/11925) by [@tiangolo](https://github.com/tiangolo).
* 👷 Update tokens for GitHub Actions. PR [#11924](https://github.com/fastapi/fastapi/pull/11924) by [@tiangolo](https://github.com/tiangolo).
* 👷 Update token permissions to comment deployment URL in docs. PR [#11917](https://github.com/fastapi/fastapi/pull/11917) by [@tiangolo](https://github.com/tiangolo).
* 👷 Update token permissions for GitHub Actions. PR [#11915](https://github.com/fastapi/fastapi/pull/11915) by [@tiangolo](https://github.com/tiangolo).
* 👷 Update GitHub Actions token usage. PR [#11914](https://github.com/fastapi/fastapi/pull/11914) by [@tiangolo](https://github.com/tiangolo).
* 👷 Update GitHub Action to notify translations with label `approved-1`. PR [#11907](https://github.com/tiangolo/fastapi/pull/11907) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Update sponsors, remove Reflex. PR [#11875](https://github.com/tiangolo/fastapi/pull/11875) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Update sponsors: remove TalkPython. PR [#11861](https://github.com/tiangolo/fastapi/pull/11861) by [@tiangolo](https://github.com/tiangolo).
* 🔨 Update docs Termynal scripts to not include line nums for local dev. PR [#11854](https://github.com/tiangolo/fastapi/pull/11854) by [@tiangolo](https://github.com/tiangolo).

## 0.111.1 (2024-07-14)

### Upgrades

* ➖ Remove `orjson` and `ujson` from default dependencies. PR [#11842](https://github.com/tiangolo/fastapi/pull/11842) by [@tiangolo](https://github.com/tiangolo).
    * These dependencies are still installed when you install with `pip install "fastapi[all]"`. But they are not included in `pip install fastapi`.
* 📝 Restored Swagger-UI links to use the latest version possible. PR [#11459](https://github.com/tiangolo/fastapi/pull/11459) by [@UltimateLobster](https://github.com/UltimateLobster).

### Docs

* ✏️ Rewording in `docs/en/docs/fastapi-cli.md`. PR [#11716](https://github.com/tiangolo/fastapi/pull/11716) by [@alejsdev](https://github.com/alejsdev).
* 📝 Update Hypercorn links in all the docs. PR [#11744](https://github.com/tiangolo/fastapi/pull/11744) by [@kittydoor](https://github.com/kittydoor).
* 📝  Update docs with Ariadne reference from Starlette to FastAPI. PR [#11797](https://github.com/tiangolo/fastapi/pull/11797) by [@DamianCzajkowski](https://github.com/DamianCzajkowski).
* 📝 Update fastapi instrumentation external link. PR [#11317](https://github.com/tiangolo/fastapi/pull/11317) by [@softwarebloat](https://github.com/softwarebloat).
* ✏️ Fix links to alembic example repo in docs. PR [#11628](https://github.com/tiangolo/fastapi/pull/11628) by [@augiwan](https://github.com/augiwan).
* ✏️ Update `docs/en/docs/fastapi-cli.md`. PR [#11715](https://github.com/tiangolo/fastapi/pull/11715) by [@alejsdev](https://github.com/alejsdev).
* 📝 Update External Links . PR [#11500](https://github.com/tiangolo/fastapi/pull/11500) by [@devon2018](https://github.com/devon2018).
* 📝 Add External Link: Tutorial de FastAPI, ¿el mejor framework de Python?. PR [#11618](https://github.com/tiangolo/fastapi/pull/11618) by [@EduardoZepeda](https://github.com/EduardoZepeda).
* 📝 Fix typo in `docs/en/docs/tutorial/body-multiple-params.md`. PR [#11698](https://github.com/tiangolo/fastapi/pull/11698) by [@mwb-u](https://github.com/mwb-u).
* 📝 Add External Link: Deploy a Serverless FastAPI App with Neon Postgres and AWS App Runner at any scale. PR [#11633](https://github.com/tiangolo/fastapi/pull/11633) by [@ananis25](https://github.com/ananis25).
* 📝 Update `security/first-steps.md`. PR [#11674](https://github.com/tiangolo/fastapi/pull/11674) by [@alejsdev](https://github.com/alejsdev).
* 📝 Update `security/first-steps.md`. PR [#11673](https://github.com/tiangolo/fastapi/pull/11673) by [@alejsdev](https://github.com/alejsdev).
* 📝 Update note in `path-params-numeric-validations.md`. PR [#11672](https://github.com/tiangolo/fastapi/pull/11672) by [@alejsdev](https://github.com/alejsdev).
* 📝 Tweak intro docs about `Annotated` and `Query()` params. PR [#11664](https://github.com/tiangolo/fastapi/pull/11664) by [@tiangolo](https://github.com/tiangolo).
* 📝 Update JWT auth documentation to use PyJWT instead of pyhon-jose. PR [#11589](https://github.com/tiangolo/fastapi/pull/11589) by [@estebanx64](https://github.com/estebanx64).
* 📝 Update docs. PR [#11603](https://github.com/tiangolo/fastapi/pull/11603) by [@alejsdev](https://github.com/alejsdev).
* ✏️ Fix typo: convert every 're-use' to 'reuse'.. PR [#11598](https://github.com/tiangolo/fastapi/pull/11598) by [@hasansezertasan](https://github.com/hasansezertasan).
* ✏️ Fix typo in `fastapi/applications.py`. PR [#11593](https://github.com/tiangolo/fastapi/pull/11593) by [@petarmaric](https://github.com/petarmaric).
* ✏️ Fix link in `fastapi-cli.md`. PR [#11524](https://github.com/tiangolo/fastapi/pull/11524) by [@svlandeg](https://github.com/svlandeg).

### Translations

* 🌐 Add Spanish translation for `docs/es/docs/how-to/graphql.md`. PR [#11697](https://github.com/tiangolo/fastapi/pull/11697) by [@camigomezdev](https://github.com/camigomezdev).
* 🌐 Add Portuguese translation for `docs/pt/docs/reference/index.md`. PR [#11840](https://github.com/tiangolo/fastapi/pull/11840) by [@lucasbalieiro](https://github.com/lucasbalieiro).
* 🌐 Fix link in German translation. PR [#11836](https://github.com/tiangolo/fastapi/pull/11836) by [@anitahammer](https://github.com/anitahammer).
* 🌐 Add Portuguese translation for `docs/pt/docs/tutorial/dependencies/sub-dependencies.md`. PR [#11792](https://github.com/tiangolo/fastapi/pull/11792) by [@Joao-Pedro-P-Holanda](https://github.com/Joao-Pedro-P-Holanda).
* 🌐 Add Turkish translation for `docs/tr/docs/tutorial/request-forms.md`. PR [#11553](https://github.com/tiangolo/fastapi/pull/11553) by [@hasansezertasan](https://github.com/hasansezertasan).
* 🌐 Add Portuguese translation for `docs/pt/docs/reference/exceptions.md`. PR [#11834](https://github.com/tiangolo/fastapi/pull/11834) by [@lucasbalieiro](https://github.com/lucasbalieiro).
* 🌐 Add Portuguese translation for `docs/pt/docs/tutorial/dependencies/global-dependencies.md`. PR [#11826](https://github.com/tiangolo/fastapi/pull/11826) by [@Joao-Pedro-P-Holanda](https://github.com/Joao-Pedro-P-Holanda).
* 🌐 Add Portuguese translation for `docs/pt/docs/how-to/general.md`. PR [#11825](https://github.com/tiangolo/fastapi/pull/11825) by [@lucasbalieiro](https://github.com/lucasbalieiro).
* 🌐 Add Portuguese translation for `docs/pt/docs/advanced/async-tests.md`. PR [#11808](https://github.com/tiangolo/fastapi/pull/11808) by [@ceb10n](https://github.com/ceb10n).
* 🌐 Add Ukrainian translation for `docs/uk/docs/tutorial/first-steps.md`. PR [#11809](https://github.com/tiangolo/fastapi/pull/11809) by [@vkhoroshchak](https://github.com/vkhoroshchak).
* 🌐 Add Portuguese translation for `docs/pt/docs/tutorial/dependencies/dependencies-in-path-operation-operators.md`. PR [#11804](https://github.com/tiangolo/fastapi/pull/11804) by [@Joao-Pedro-P-Holanda](https://github.com/Joao-Pedro-P-Holanda).
* 🌐 Add Chinese translation for `docs/zh/docs/fastapi-cli.md`. PR [#11786](https://github.com/tiangolo/fastapi/pull/11786) by [@logan2d5](https://github.com/logan2d5).
* 🌐 Add Portuguese translation for `docs/pt/docs/advanced/openapi-webhooks.md`. PR [#11791](https://github.com/tiangolo/fastapi/pull/11791) by [@ceb10n](https://github.com/ceb10n).
* 🌐 Update Chinese translation for `docs/tutorial/security/oauth2-jwt.md`. PR [#11781](https://github.com/tiangolo/fastapi/pull/11781) by [@logan2d5](https://github.com/logan2d5).
* 📝 Fix image missing in French translation for `docs/fr/docs/async.md` . PR [#11787](https://github.com/tiangolo/fastapi/pull/11787) by [@pe-brian](https://github.com/pe-brian).
* 🌐 Add Portuguese translation for `docs/pt/docs/advanced/advanced-dependencies.md`. PR [#11775](https://github.com/tiangolo/fastapi/pull/11775) by [@ceb10n](https://github.com/ceb10n).
* 🌐 Add Portuguese translation for `docs/pt/docs/tutorial/dependencies/classes-as-dependencies.md`. PR [#11768](https://github.com/tiangolo/fastapi/pull/11768) by [@Joao-Pedro-P-Holanda](https://github.com/Joao-Pedro-P-Holanda).
* 🌐  Add Portuguese translation for `docs/pt/docs/advanced/additional-status-codes.md`. PR [#11753](https://github.com/tiangolo/fastapi/pull/11753) by [@ceb10n](https://github.com/ceb10n).
* 🌐 Add Portuguese translation for `docs/pt/docs/tutorial/dependencies/index.md`. PR [#11757](https://github.com/tiangolo/fastapi/pull/11757) by [@Joao-Pedro-P-Holanda](https://github.com/Joao-Pedro-P-Holanda).
* 🌐 Add Portuguese translation for `docs/pt/docs/advanced/settings.md`. PR [#11739](https://github.com/tiangolo/fastapi/pull/11739) by [@Joao-Pedro-P-Holanda](https://github.com/Joao-Pedro-P-Holanda).
* 🌐 Add French translation for `docs/fr/docs/learn/index.md`. PR [#11712](https://github.com/tiangolo/fastapi/pull/11712) by [@benjaminvandammeholberton](https://github.com/benjaminvandammeholberton).
* 🌐 Add Portuguese translation for `docs/pt/docs/how-to/index.md`. PR [#11731](https://github.com/tiangolo/fastapi/pull/11731) by [@vhsenna](https://github.com/vhsenna).
* 🌐 Add Portuguese translation for `docs/pt/docs/advanced/additional-responses.md`. PR [#11736](https://github.com/tiangolo/fastapi/pull/11736) by [@ceb10n](https://github.com/ceb10n).
* 🌐 Add Portuguese translation for `docs/pt/docs/advanced/benchmarks.md`. PR [#11713](https://github.com/tiangolo/fastapi/pull/11713) by [@ceb10n](https://github.com/ceb10n).
* 🌐 Fix Korean translation for `docs/ko/docs/tutorial/response-status-code.md`. PR [#11718](https://github.com/tiangolo/fastapi/pull/11718) by [@nayeonkinn](https://github.com/nayeonkinn).
* 🌐 Add Korean translation for `docs/ko/docs/tutorial/extra-data-types.md`. PR [#11711](https://github.com/tiangolo/fastapi/pull/11711) by [@nayeonkinn](https://github.com/nayeonkinn).
* 🌐 Fix Korean translation for `docs/ko/docs/tutorial/body-nested-models.md`. PR [#11710](https://github.com/tiangolo/fastapi/pull/11710) by [@nayeonkinn](https://github.com/nayeonkinn).
* 🌐 Add Portuguese translation for `docs/pt/docs/advanced/fastapi-cli.md`. PR [#11641](https://github.com/tiangolo/fastapi/pull/11641) by [@ayr-ton](https://github.com/ayr-ton).
* 🌐 Add Traditional Chinese translation for `docs/zh-hant/docs/fastapi-people.md`. PR [#11639](https://github.com/tiangolo/fastapi/pull/11639) by [@hsuanchi](https://github.com/hsuanchi).
* 🌐 Add Turkish translation for `docs/tr/docs/advanced/index.md`. PR [#11606](https://github.com/tiangolo/fastapi/pull/11606) by [@hasansezertasan](https://github.com/hasansezertasan).
* 🌐 Add Turkish translation for `docs/tr/docs/deployment/cloud.md`. PR [#11610](https://github.com/tiangolo/fastapi/pull/11610) by [@hasansezertasan](https://github.com/hasansezertasan).
* 🌐 Add Turkish translation for `docs/tr/docs/advanced/security/index.md`. PR [#11609](https://github.com/tiangolo/fastapi/pull/11609) by [@hasansezertasan](https://github.com/hasansezertasan).
* 🌐 Add Turkish translation for `docs/tr/docs/advanced/testing-websockets.md`. PR [#11608](https://github.com/tiangolo/fastapi/pull/11608) by [@hasansezertasan](https://github.com/hasansezertasan).
* 🌐 Add Turkish translation for `docs/tr/docs/how-to/general.md`. PR [#11607](https://github.com/tiangolo/fastapi/pull/11607) by [@hasansezertasan](https://github.com/hasansezertasan).
* 🌐 Update Chinese translation for `docs/zh/docs/advanced/templates.md`. PR [#11620](https://github.com/tiangolo/fastapi/pull/11620) by [@chaoless](https://github.com/chaoless).
* 🌐 Add Turkish translation for `docs/tr/docs/deployment/index.md`. PR [#11605](https://github.com/tiangolo/fastapi/pull/11605) by [@hasansezertasan](https://github.com/hasansezertasan).
* 🌐 Add Turkish translation for `docs/tr/docs/tutorial/static-files.md`. PR [#11599](https://github.com/tiangolo/fastapi/pull/11599) by [@hasansezertasan](https://github.com/hasansezertasan).
* 🌐 Polish translation for `docs/pl/docs/fastapi-people.md`. PR [#10196](https://github.com/tiangolo/fastapi/pull/10196) by [@isulim](https://github.com/isulim).
* 🌐 Add Turkish translation for `docs/tr/docs/advanced/wsgi.md`. PR [#11575](https://github.com/tiangolo/fastapi/pull/11575) by [@hasansezertasan](https://github.com/hasansezertasan).
* 🌐 Add Turkish translation for `docs/tr/docs/tutorial/cookie-params.md`. PR [#11561](https://github.com/tiangolo/fastapi/pull/11561) by [@hasansezertasan](https://github.com/hasansezertasan).
* 🌐 Add Russian translation for `docs/ru/docs/about/index.md`. PR [#10961](https://github.com/tiangolo/fastapi/pull/10961) by [@s111d](https://github.com/s111d).
* 🌐 Update Chinese translation for `docs/zh/docs/tutorial/sql-databases.md`. PR [#11539](https://github.com/tiangolo/fastapi/pull/11539) by [@chaoless](https://github.com/chaoless).
* 🌐 Add Chinese translation for `docs/zh/docs/how-to/configure-swagger-ui.md`. PR [#11501](https://github.com/tiangolo/fastapi/pull/11501) by [@Lucas-lyh](https://github.com/Lucas-lyh).
* 🌐 Update Chinese translation for `/docs/advanced/security/http-basic-auth.md`. PR [#11512](https://github.com/tiangolo/fastapi/pull/11512) by [@nick-cjyx9](https://github.com/nick-cjyx9).

### Internal

* ♻️ Simplify internal docs script. PR [#11777](https://github.com/tiangolo/fastapi/pull/11777) by [@gitworkflows](https://github.com/gitworkflows).
* 🔧 Update sponsors: add Fine. PR [#11784](https://github.com/tiangolo/fastapi/pull/11784) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Tweak sponsors: Kong URL. PR [#11765](https://github.com/tiangolo/fastapi/pull/11765) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Tweak sponsors: Kong URL. PR [#11764](https://github.com/tiangolo/fastapi/pull/11764) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Update sponsors, add Stainless. PR [#11763](https://github.com/tiangolo/fastapi/pull/11763) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Update sponsors, add Zuplo. PR [#11729](https://github.com/tiangolo/fastapi/pull/11729) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Update Sponsor link: Coherence. PR [#11730](https://github.com/tiangolo/fastapi/pull/11730) by [@tiangolo](https://github.com/tiangolo).
* 👥 Update FastAPI People. PR [#11669](https://github.com/tiangolo/fastapi/pull/11669) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Add sponsor Kong. PR [#11662](https://github.com/tiangolo/fastapi/pull/11662) by [@tiangolo](https://github.com/tiangolo).
* 👷 Update Smokeshow, fix sync download artifact and smokeshow configs. PR [#11563](https://github.com/tiangolo/fastapi/pull/11563) by [@tiangolo](https://github.com/tiangolo).
* 👷 Update Smokeshow download artifact GitHub Action. PR [#11562](https://github.com/tiangolo/fastapi/pull/11562) by [@tiangolo](https://github.com/tiangolo).
* 👷 Update GitHub actions to download and upload artifacts to v4, for docs and coverage. PR [#11550](https://github.com/tiangolo/fastapi/pull/11550) by [@tamird](https://github.com/tamird).
* 👷 Tweak CI for test-redistribute, add needed env vars for slim. PR [#11549](https://github.com/tiangolo/fastapi/pull/11549) by [@tiangolo](https://github.com/tiangolo).
* 👥 Update FastAPI People. PR [#11511](https://github.com/tiangolo/fastapi/pull/11511) by [@tiangolo](https://github.com/tiangolo).

## 0.111.0 (2024-05-03)

### Features

* ✨ Add FastAPI CLI, the new `fastapi` command. PR [#11522](https://github.com/tiangolo/fastapi/pull/11522) by [@tiangolo](https://github.com/tiangolo).
    * New docs: [FastAPI CLI](https://fastapi.tiangolo.com/fastapi-cli/).

Try it out with:

```console
$ pip install --upgrade fastapi

$ fastapi dev main.py

 ╭────────── FastAPI CLI - Development mode ───────────╮
 │                                                     │
 │  Serving at: http://127.0.0.1:8000                  │
 │                                                     │
 │  API docs: http://127.0.0.1:8000/docs               │
 │                                                     │
 │  Running in development mode, for production use:   │
 │                                                     │
 │  fastapi run                                        │
 │                                                     │
 ╰─────────────────────────────────────────────────────╯

INFO:     Will watch for changes in these directories: ['/home/user/code/awesomeapp']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [2248755] using WatchFiles
INFO:     Started server process [2248757]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Refactors

* 🔧 Add configs and setup for `fastapi-slim` including optional extras `fastapi-slim[standard]`, and `fastapi` including by default the same `standard` extras. PR [#11503](https://github.com/tiangolo/fastapi/pull/11503) by [@tiangolo](https://github.com/tiangolo).

## 0.110.3 (2024-04-30)

### Docs

* 📝 Update references to Python version, FastAPI supports all the current versions, no need to make the version explicit. PR [#11496](https://github.com/tiangolo/fastapi/pull/11496) by [@tiangolo](https://github.com/tiangolo).
* ✏️ Fix typo in `fastapi/security/api_key.py`. PR [#11481](https://github.com/tiangolo/fastapi/pull/11481) by [@ch33zer](https://github.com/ch33zer).
* ✏️ Fix typo in `security/http.py`. PR [#11455](https://github.com/tiangolo/fastapi/pull/11455) by [@omarmoo5](https://github.com/omarmoo5).

### Translations

* 🌐 Add Traditional Chinese translation for `docs/zh-hant/benchmarks.md`. PR [#11484](https://github.com/tiangolo/fastapi/pull/11484) by [@KNChiu](https://github.com/KNChiu).
* 🌐 Update Chinese translation for `docs/zh/docs/fastapi-people.md`. PR [#11476](https://github.com/tiangolo/fastapi/pull/11476) by [@billzhong](https://github.com/billzhong).
* 🌐 Add Chinese translation for `docs/zh/docs/how-to/index.md` and `docs/zh/docs/how-to/general.md`. PR [#11443](https://github.com/tiangolo/fastapi/pull/11443) by [@billzhong](https://github.com/billzhong).
* 🌐 Add Spanish translation for cookie-params `docs/es/docs/tutorial/cookie-params.md`. PR [#11410](https://github.com/tiangolo/fastapi/pull/11410) by [@fabianfalon](https://github.com/fabianfalon).

### Internal

* ⬆ Bump mkdocstrings[python] from 0.23.0 to 0.24.3. PR [#11469](https://github.com/tiangolo/fastapi/pull/11469) by [@dependabot[bot]](https://github.com/apps/dependabot).
* 🔨 Update internal scripts and remove unused ones. PR [#11499](https://github.com/tiangolo/fastapi/pull/11499) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Migrate from Hatch to PDM for the internal build. PR [#11498](https://github.com/tiangolo/fastapi/pull/11498) by [@tiangolo](https://github.com/tiangolo).
* ⬆️ Upgrade MkDocs Material and re-enable cards. PR [#11466](https://github.com/tiangolo/fastapi/pull/11466) by [@tiangolo](https://github.com/tiangolo).
* ⬆ Bump pillow from 10.2.0 to 10.3.0. PR [#11403](https://github.com/tiangolo/fastapi/pull/11403) by [@dependabot[bot]](https://github.com/apps/dependabot).
* 🔧 Ungroup dependabot updates. PR [#11465](https://github.com/tiangolo/fastapi/pull/11465) by [@tiangolo](https://github.com/tiangolo).

## 0.110.2 (2024-04-19)

### Fixes

* 🐛 Fix support for query parameters with list types, handle JSON encoding Pydantic `UndefinedType`. PR [#9929](https://github.com/tiangolo/fastapi/pull/9929) by [@arjwilliams](https://github.com/arjwilliams).

### Refactors

* ♻️ Simplify Pydantic configs in OpenAPI models in `fastapi/openapi/models.py`. PR [#10886](https://github.com/tiangolo/fastapi/pull/10886) by [@JoeTanto2](https://github.com/JoeTanto2).
* ✨ Add support for Pydantic's 2.7 new deprecated Field parameter, remove URL from validation errors response. PR [#11461](https://github.com/tiangolo/fastapi/pull/11461) by [@tiangolo](https://github.com/tiangolo).

### Docs

* 📝 Fix types in examples under `docs_src/extra_data_types`. PR [#10535](https://github.com/tiangolo/fastapi/pull/10535) by [@nilslindemann](https://github.com/nilslindemann).
* 📝 Update references to UJSON. PR [#11464](https://github.com/tiangolo/fastapi/pull/11464) by [@tiangolo](https://github.com/tiangolo).
* 📝 Tweak docs and translations links, typos, format. PR [#11389](https://github.com/tiangolo/fastapi/pull/11389) by [@nilslindemann](https://github.com/nilslindemann).
* 📝 Fix typo in `docs/es/docs/async.md`. PR [#11400](https://github.com/tiangolo/fastapi/pull/11400) by [@fabianfalon](https://github.com/fabianfalon).
* 📝 Update OpenAPI client generation docs to use `@hey-api/openapi-ts`. PR [#11339](https://github.com/tiangolo/fastapi/pull/11339) by [@jordanshatford](https://github.com/jordanshatford).

### Translations

* 🌐 Update Chinese translation for `docs/zh/docs/index.html`. PR [#11430](https://github.com/tiangolo/fastapi/pull/11430) by [@waketzheng](https://github.com/waketzheng).
* 🌐 Add Russian translation for `docs/ru/docs/tutorial/dependencies/dependencies-in-path-operation-decorators.md`. PR [#11411](https://github.com/tiangolo/fastapi/pull/11411) by [@anton2yakovlev](https://github.com/anton2yakovlev).
* 🌐 Add Portuguese translations for `learn/index.md` `resources/index.md` `help/index.md` `about/index.md`. PR [#10807](https://github.com/tiangolo/fastapi/pull/10807) by [@nazarepiedady](https://github.com/nazarepiedady).
* 🌐 Update Russian translations for deployments docs. PR [#11271](https://github.com/tiangolo/fastapi/pull/11271) by [@Lufa1u](https://github.com/Lufa1u).
* 🌐 Add Bengali translations for `docs/bn/docs/python-types.md`. PR [#11376](https://github.com/tiangolo/fastapi/pull/11376) by [@imtiaz101325](https://github.com/imtiaz101325).
* 🌐 Add Korean translation for `docs/ko/docs/tutorial/security/simple-oauth2.md`. PR [#5744](https://github.com/tiangolo/fastapi/pull/5744) by [@KdHyeon0661](https://github.com/KdHyeon0661).
* 🌐 Add Korean translation for `docs/ko/docs/help-fastapi.md`. PR [#4139](https://github.com/tiangolo/fastapi/pull/4139) by [@kty4119](https://github.com/kty4119).
* 🌐 Add Korean translation for `docs/ko/docs/advanced/events.md`. PR [#5087](https://github.com/tiangolo/fastapi/pull/5087) by [@pers0n4](https://github.com/pers0n4).
* 🌐 Add Japanese translation for `docs/ja/docs/tutorial/path-operation-configuration.md`. PR [#1954](https://github.com/tiangolo/fastapi/pull/1954) by [@SwftAlpc](https://github.com/SwftAlpc).
* 🌐 Add Japanese translation for `docs/ja/docs/tutorial/request-forms-and-files.md`. PR [#1946](https://github.com/tiangolo/fastapi/pull/1946) by [@SwftAlpc](https://github.com/SwftAlpc).
* 🌐 Add Russian translation for `docs/ru/docs/tutorial/dependencies/dependencies-with-yield.md`. PR [#10532](https://github.com/tiangolo/fastapi/pull/10532) by [@AlertRED](https://github.com/AlertRED).
* 🌐 Add Korean translation for `docs/ko/docs/tutorial/debugging.md`. PR [#5695](https://github.com/tiangolo/fastapi/pull/5695) by [@JungWooGeon](https://github.com/JungWooGeon).

### Internal

* ⬆️ Upgrade version of typer for docs. PR [#11393](https://github.com/tiangolo/fastapi/pull/11393) by [@tiangolo](https://github.com/tiangolo).

## 0.110.1 (2024-04-02)

### Fixes

* 🐛 Fix parameterless `Depends()` with generics. PR [#9479](https://github.com/tiangolo/fastapi/pull/9479) by [@nzig](https://github.com/nzig).

### Refactors

* ♻️ Update mypy. PR [#11049](https://github.com/tiangolo/fastapi/pull/11049) by [@k0t3n](https://github.com/k0t3n).
* ♻️ Simplify string format with f-strings in `fastapi/applications.py`. PR [#11335](https://github.com/tiangolo/fastapi/pull/11335) by [@igeni](https://github.com/igeni).

### Upgrades

* ⬆️ Upgrade Starlette to >=0.37.2,= 0.36.3`. PR [#11086](https://github.com/tiangolo/fastapi/pull/11086) by [@tiangolo](https://github.com/tiangolo).

### Translations

* 🌐 Update Turkish translation for `docs/tr/docs/fastapi-people.md`. PR [#10547](https://github.com/tiangolo/fastapi/pull/10547) by [@alperiox](https://github.com/alperiox).

### Internal

* 🍱 Add new FastAPI logo. PR [#11090](https://github.com/tiangolo/fastapi/pull/11090) by [@tiangolo](https://github.com/tiangolo).

## 0.109.1 (2024-02-03)

### Security fixes

* ⬆️ Upgrade minimum version of `python-multipart` to `>=0.0.7` to fix a vulnerability when using form data with a ReDos attack. You can also simply upgrade `python-multipart`.

Read more in the [advisory: Content-Type Header ReDoS](https://github.com/tiangolo/fastapi/security/advisories/GHSA-qf9m-vfgh-m389).

### Features

* ✨  Include HTTP 205 in status codes with no body. PR [#10969](https://github.com/tiangolo/fastapi/pull/10969) by [@tiangolo](https://github.com/tiangolo).

### Refactors

* ✅ Refactor tests for duplicate operation ID generation for compatibility with other tools running the FastAPI test suite. PR [#10876](https://github.com/tiangolo/fastapi/pull/10876) by [@emmettbutler](https://github.com/emmettbutler).
* ♻️ Simplify string format with f-strings in `fastapi/utils.py`. PR [#10576](https://github.com/tiangolo/fastapi/pull/10576) by [@eukub](https://github.com/eukub).
* 🔧 Fix Ruff configuration unintentionally enabling and re-disabling mccabe complexity check. PR [#10893](https://github.com/tiangolo/fastapi/pull/10893) by [@jiridanek](https://github.com/jiridanek).
* ✅ Re-enable test in `tests/test_tutorial/test_header_params/test_tutorial003.py` after fix in Starlette. PR [#10904](https://github.com/tiangolo/fastapi/pull/10904) by [@ooknimm](https://github.com/ooknimm).

### Docs

* 📝 Tweak wording in `help-fastapi.md`. PR [#11040](https://github.com/tiangolo/fastapi/pull/11040) by [@tiangolo](https://github.com/tiangolo).
* 📝 Tweak docs for Behind a Proxy. PR [#11038](https://github.com/tiangolo/fastapi/pull/11038) by [@tiangolo](https://github.com/tiangolo).
* 📝 Add External Link: 10 Tips for adding SQLAlchemy to FastAPI. PR [#11036](https://github.com/tiangolo/fastapi/pull/11036) by [@Donnype](https://github.com/Donnype).
* 📝 Add External Link: Tips on migrating from Flask to FastAPI and vice-versa. PR [#11029](https://github.com/tiangolo/fastapi/pull/11029) by [@jtemporal](https://github.com/jtemporal).
* 📝 Deprecate old tutorials: Peewee, Couchbase, encode/databases. PR [#10979](https://github.com/tiangolo/fastapi/pull/10979) by [@tiangolo](https://github.com/tiangolo).
* ✏️ Fix typo in `fastapi/security/oauth2.py`. PR [#10972](https://github.com/tiangolo/fastapi/pull/10972) by [@RafalSkolasinski](https://github.com/RafalSkolasinski).
* 📝 Update `HTTPException` details in `docs/en/docs/tutorial/handling-errors.md`. PR [#5418](https://github.com/tiangolo/fastapi/pull/5418) by [@papb](https://github.com/papb).
* ✏️ A few tweaks in `docs/de/docs/tutorial/first-steps.md`. PR [#10959](https://github.com/tiangolo/fastapi/pull/10959) by [@nilslindemann](https://github.com/nilslindemann).
* ✏️ Fix link in `docs/en/docs/advanced/async-tests.md`. PR [#10960](https://github.com/tiangolo/fastapi/pull/10960) by [@nilslindemann](https://github.com/nilslindemann).
* ✏️ Fix typos for Spanish documentation. PR [#10957](https://github.com/tiangolo/fastapi/pull/10957) by [@jlopezlira](https://github.com/jlopezlira).
* 📝 Add warning about lifespan functions and backwards compatibility with events. PR [#10734](https://github.com/tiangolo/fastapi/pull/10734) by [@jacob-indigo](https://github.com/jacob-indigo).
* ✏️ Fix broken link in `docs/tutorial/sql-databases.md` in several languages. PR [#10716](https://github.com/tiangolo/fastapi/pull/10716) by [@theoohoho](https://github.com/theoohoho).
* ✏️ Remove broken links from `external_links.yml`. PR [#10943](https://github.com/tiangolo/fastapi/pull/10943) by [@Torabek](https://github.com/Torabek).
* 📝 Update template docs with more info about `url_for`. PR [#5937](https://github.com/tiangolo/fastapi/pull/5937) by [@EzzEddin](https://github.com/EzzEddin).
* 📝 Update usage of Token model in security docs. PR [#9313](https://github.com/tiangolo/fastapi/pull/9313) by [@piotrszacilowski](https://github.com/piotrszacilowski).
* ✏️ Update highlighted line in `docs/en/docs/tutorial/bigger-applications.md`. PR [#5490](https://github.com/tiangolo/fastapi/pull/5490) by [@papb](https://github.com/papb).
* 📝 Add External Link: Explore How to Effectively Use JWT With FastAPI. PR [#10212](https://github.com/tiangolo/fastapi/pull/10212) by [@aanchlia](https://github.com/aanchlia).
* 📝 Add hyperlink to `docs/en/docs/tutorial/static-files.md`. PR [#10243](https://github.com/tiangolo/fastapi/pull/10243) by [@hungtsetse](https://github.com/hungtsetse).
* 📝 Add External Link: Instrument a FastAPI service adding tracing with OpenTelemetry and send/show traces in Grafana Tempo. PR [#9440](https://github.com/tiangolo/fastapi/pull/9440) by [@softwarebloat](https://github.com/softwarebloat).
* 📝 Review and rewording of `en/docs/contributing.md`. PR [#10480](https://github.com/tiangolo/fastapi/pull/10480) by [@nilslindemann](https://github.com/nilslindemann).
* 📝 Add External Link: ML serving and monitoring with FastAPI and Evidently. PR [#9701](https://github.com/tiangolo/fastapi/pull/9701) by [@mnrozhkov](https://github.com/mnrozhkov).
* 📝 Reword in docs, from "have in mind" to "keep in mind". PR [#10376](https://github.com/tiangolo/fastapi/pull/10376) by [@malicious](https://github.com/malicious).
* 📝 Add External Link: Talk by Jeny Sadadia. PR [#10265](https://github.com/tiangolo/fastapi/pull/10265) by [@JenySadadia](https://github.com/JenySadadia).
* 📝 Add location info to `tutorial/bigger-applications.md`. PR [#10552](https://github.com/tiangolo/fastapi/pull/10552) by [@nilslindemann](https://github.com/nilslindemann).
* ✏️ Fix Pydantic method name in `docs/en/docs/advanced/path-operation-advanced-configuration.md`. PR [#10826](https://github.com/tiangolo/fastapi/pull/10826) by [@ahmedabdou14](https://github.com/ahmedabdou14).

### Translations

* 🌐 Add Spanish translation for `docs/es/docs/external-links.md`. PR [#10933](https://github.com/tiangolo/fastapi/pull/10933) by [@pablocm83](https://github.com/pablocm83).
* 🌐 Update Korean translation for `docs/ko/docs/tutorial/first-steps.md`, `docs/ko/docs/tutorial/index.md`, `docs/ko/docs/tutorial/path-params.md`, and `docs/ko/docs/tutorial/query-params.md`. PR [#4218](https://github.com/tiangolo/fastapi/pull/4218) by [@SnowSuno](https://github.com/SnowSuno).
* 🌐 Add Chinese translation for `docs/zh/docs/tutorial/dependencies/dependencies-with-yield.md`. PR [#10870](https://github.com/tiangolo/fastapi/pull/10870) by [@zhiquanchi](https://github.com/zhiquanchi).
* 🌐 Add Chinese translation for `docs/zh/docs/deployment/concepts.md`. PR [#10282](https://github.com/tiangolo/fastapi/pull/10282) by [@xzmeng](https://github.com/xzmeng).
* 🌐 Add Azerbaijani translation for `docs/az/docs/index.md`. PR [#11047](https://github.com/tiangolo/fastapi/pull/11047) by [@aykhans](https://github.com/aykhans).
* 🌐 Add Korean translation for `docs/ko/docs/tutorial/middleware.md`. PR [#2829](https://github.com/tiangolo/fastapi/pull/2829) by [@JeongHyeongKim](https://github.com/JeongHyeongKim).
* 🌐 Add German translation for `docs/de/docs/tutorial/body-nested-models.md`. PR [#10313](https://github.com/tiangolo/fastapi/pull/10313) by [@nilslindemann](https://github.com/nilslindemann).
* 🌐 Add Persian translation for `docs/fa/docs/tutorial/middleware.md`. PR [#9695](https://github.com/tiangolo/fastapi/pull/9695) by [@mojtabapaso](https://github.com/mojtabapaso).
* 🌐 Update Farsi translation for `docs/fa/docs/index.md`. PR [#10216](https://github.com/tiangolo/fastapi/pull/10216) by [@theonlykingpin](https://github.com/theonlykingpin).
* 🌐 Add German translation for `docs/de/docs/tutorial/body-fields.md`. PR [#10310](https://github.com/tiangolo/fastapi/pull/10310) by [@nilslindemann](https://github.com/nilslindemann).
* 🌐 Add German translation for `docs/de/docs/tutorial/body.md`. PR [#10295](https://github.com/tiangolo/fastapi/pull/10295) by [@nilslindemann](https://github.com/nilslindemann).
* 🌐 Add German translation for `docs/de/docs/tutorial/body-multiple-params.md`. PR [#10308](https://github.com/tiangolo/fastapi/pull/10308) by [@nilslindemann](https://github.com/nilslindemann).
* 🌐 Add Japanese translation for `docs/ja/docs/tutorial/security/get-current-user.md`. PR [#2681](https://github.com/tiangolo/fastapi/pull/2681) by [@sh0nk](https://github.com/sh0nk).
* 🌐 Add Chinese translation for `docs/zh/docs/advanced/advanced-dependencies.md`. PR [#3798](https://github.com/tiangolo/fastapi/pull/3798) by [@jaystone776](https://github.com/jaystone776).
* 🌐 Add Chinese translation for `docs/zh/docs/advanced/events.md`. PR [#3815](https://github.com/tiangolo/fastapi/pull/3815) by [@jaystone776](https://github.com/jaystone776).
* 🌐 Add Chinese translation for `docs/zh/docs/advanced/behind-a-proxy.md`. PR [#3820](https://github.com/tiangolo/fastapi/pull/3820) by [@jaystone776](https://github.com/jaystone776).
* 🌐 Add Chinese translation for `docs/zh/docs/advanced/testing-events.md`. PR [#3818](https://github.com/tiangolo/fastapi/pull/3818) by [@jaystone776](https://github.com/jaystone776).
* 🌐 Add Chinese translation for `docs/zh/docs/advanced/testing-websockets.md`. PR [#3817](https://github.com/tiangolo/fastapi/pull/3817) by [@jaystone776](https://github.com/jaystone776).
* 🌐 Add Chinese translation for `docs/zh/docs/advanced/testing-database.md`. PR [#3821](https://github.com/tiangolo/fastapi/pull/3821) by [@jaystone776](https://github.com/jaystone776).
* 🌐 Add Chinese translation for `docs/zh/docs/deployment/deta.md`. PR [#3837](https://github.com/tiangolo/fastapi/pull/3837) by [@jaystone776](https://github.com/jaystone776).
* 🌐 Add Chinese translation for `docs/zh/docs/history-design-future.md`. PR [#3832](https://github.com/tiangolo/fastapi/pull/3832) by [@jaystone776](https://github.com/jaystone776).
* 🌐 Add Chinese translation for `docs/zh/docs/project-generation.md`. PR [#3831](https://github.com/tiangolo/fastapi/pull/3831) by [@jaystone776](https://github.com/jaystone776).
* 🌐 Add Chinese translation for `docs/zh/docs/deployment/docker.md`. PR [#10296](https://github.com/tiangolo/fastapi/pull/10296) by [@xzmeng](https://github.com/xzmeng).
* 🌐 Update Spanish translation for `docs/es/docs/features.md`. PR [#10884](https://github.com/tiangolo/fastapi/pull/10884) by [@pablocm83](https://github.com/pablocm83).
* 🌐 Add Spanish translation for `docs/es/docs/newsletter.md`. PR [#10922](https://github.com/tiangolo/fastapi/pull/10922) by [@pablocm83](https://github.com/pablocm83).
* 🌐 Add Korean translation for `docs/ko/docs/tutorial/background-tasks.md`. PR [#5910](https://github.com/tiangolo/fastapi/pull/5910) by [@junah201](https://github.com/junah201).
* :globe_with_meridians: Add Turkish translation for `docs/tr/docs/alternatives.md`. PR [#10502](https://github.com/tiangolo/fastapi/pull/10502) by [@alperiox](https://github.com/alperiox).
* 🌐 Add Korean translation for `docs/ko/docs/tutorial/dependencies/index.md`. PR [#10989](https://github.com/tiangolo/fastapi/pull/10989) by [@KaniKim](https://github.com/KaniKim).
* 🌐 Add Korean translation for `/docs/ko/docs/tutorial/body.md`. PR [#11000](https://github.com/tiangolo/fastapi/pull/11000) by [@KaniKim](https://github.com/KaniKim).
* 🌐 Add Portuguese translation for `docs/pt/docs/tutorial/schema-extra-example.md`. PR [#4065](https://github.com/tiangolo/fastapi/pull/4065) by [@luccasmmg](https://github.com/luccasmmg).
* 🌐 Add Turkish translation for `docs/tr/docs/history-design-future.md`. PR [#11012](https://github.com/tiangolo/fastapi/pull/11012) by [@hasansezertasan](https://github.com/hasansezertasan).
* 🌐 Add Turkish translation for `docs/tr/docs/resources/index.md`. PR [#11020](https://github.com/tiangolo/fastapi/pull/11020) by [@hasansezertasan](https://github.com/hasansezertasan).
* 🌐 Add Turkish translation for `docs/tr/docs/how-to/index.md`. PR [#11021](https://github.com/tiangolo/fastapi/pull/11021) by [@hasansezertasan](https://github.com/hasansezertasan).
* 🌐 Add German translation for `docs/de/docs/tutorial/query-params.md`. PR [#10293](https://github.com/tiangolo/fastapi/pull/10293) by [@nilslindemann](https://github.com/nilslindemann).
* 🌐 Add German translation for `docs/de/docs/benchmarks.md`. PR [#10866](https://github.com/tiangolo/fastapi/pull/10866) by [@nilslindemann](https://github.com/nilslindemann).
* 🌐 Add Turkish translation for `docs/tr/docs/learn/index.md`. PR [#11014](https://github.com/tiangolo/fastapi/pull/11014) by [@hasansezertasan](https://github.com/hasansezertasan).
* 🌐 Add Persian translation for `docs/fa/docs/tutorial/security/index.md`. PR [#9945](https://github.com/tiangolo/fastapi/pull/9945) by [@mojtabapaso](https://github.com/mojtabapaso).
* 🌐 Add Turkish translation for `docs/tr/docs/help/index.md`. PR [#11013](https://github.com/tiangolo/fastapi/pull/11013) by [@hasansezertasan](https://github.com/hasansezertasan).
* 🌐 Add Turkish translation for `docs/tr/docs/about/index.md`. PR [#11006](https://github.com/tiangolo/fastapi/pull/11006) by [@hasansezertasan](https://github.com/hasansezertasan).
* 🌐 Update Turkish translation for `docs/tr/docs/benchmarks.md`. PR [#11005](https://github.com/tiangolo/fastapi/pull/11005) by [@hasansezertasan](https://github.com/hasansezertasan).
* 🌐 Add Italian translation for `docs/it/docs/index.md`. PR [#5233](https://github.com/tiangolo/fastapi/pull/5233) by [@matteospanio](https://github.com/matteospanio).
* 🌐 Add Korean translation for `docs/ko/docs/help/index.md`. PR [#10983](https://github.com/tiangolo/fastapi/pull/10983) by [@KaniKim](https://github.com/KaniKim).
* 🌐 Add Korean translation for `docs/ko/docs/features.md`. PR [#10976](https://github.com/tiangolo/fastapi/pull/10976) by [@KaniKim](https://github.com/KaniKim).
* 🌐 Add Korean translation for `docs/ko/docs/tutorial/security/get-current-user.md`. PR [#5737](https://github.com/tiangolo/fastapi/pull/5737) by [@KdHyeon0661](https://github.com/KdHyeon0661).
* 🌐 Add Russian translation for `docs/ru/docs/tutorial/security/first-steps.md`. PR [#10541](https://github.com/tiangolo/fastapi/pull/10541) by [@AlertRED](https://github.com/AlertRED).
* 🌐 Add Russian translation for `docs/ru/docs/tutorial/handling-errors.md`. PR [#10375](https://github.com/tiangolo/fastapi/pull/10375) by [@AlertRED](https://github.com/AlertRED).
* 🌐 Add Russian translation for `docs/ru/docs/tutorial/encoder.md`. PR [#10374](https://github.com/tiangolo/fastapi/pull/10374) by [@AlertRED](https://github.com/AlertRED).
* 🌐 Add Russian translation for `docs/ru/docs/tutorial/body-updates.md`. PR [#10373](https://github.com/tiangolo/fastapi/pull/10373) by [@AlertRED](https://github.com/AlertRED).
* 🌐 Russian translation: updated `fastapi-people.md`.. PR [#10255](https://github.com/tiangolo/fastapi/pull/10255) by [@NiKuma0](https://github.com/NiKuma0).
* 🌐 Add Japanese translation for `docs/ja/docs/tutorial/security/index.md`. PR [#5798](https://github.com/tiangolo/fastapi/pull/5798) by [@3w36zj6](https://github.com/3w36zj6).
* 🌐 Add German translation for `docs/de/docs/advanced/generate-clients.md`. PR [#10725](https://github.com/tiangolo/fastapi/pull/10725) by [@nilslindemann](https://github.com/nilslindemann).
* 🌐 Add German translation for `docs/de/docs/advanced/openapi-webhooks.md`. PR [#10712](https://github.com/tiangolo/fastapi/pull/10712) by [@nilslindemann](https://github.com/nilslindemann).
* 🌐 Add German translation for `docs/de/docs/advanced/custom-response.md`. PR [#10624](https://github.com/tiangolo/fastapi/pull/10624) by [@nilslindemann](https://github.com/nilslindemann).
* 🌐 Add German translation for `docs/de/docs/advanced/additional-status-codes.md`. PR [#10617](https://github.com/tiangolo/fastapi/pull/10617) by [@nilslindemann](https://github.com/nilslindemann).
* 🌐 Add German translation for `docs/de/docs/tutorial/middleware.md`. PR [#10391](https://github.com/tiangolo/fastapi/pull/10391) by [@JohannesJungbluth](https://github.com/JohannesJungbluth).
* 🌐 Add German translation for introduction documents. PR [#10497](https://github.com/tiangolo/fastapi/pull/10497) by [@nilslindemann](https://github.com/nilslindemann).
* 🌐 Add Japanese translation for `docs/ja/docs/tutorial/encoder.md`. PR [#1955](https://github.com/tiangolo/fastapi/pull/1955) by [@SwftAlpc](https://github.com/SwftAlpc).
* 🌐 Add Japanese translation for `docs/ja/docs/tutorial/extra-data-types.md`. PR [#1932](https://github.com/tiangolo/fastapi/pull/1932) by [@SwftAlpc](https://github.com/SwftAlpc).
* 🌐 Add Turkish translation for `docs/tr/docs/async.md`. PR [#5191](https://github.com/tiangolo/fastapi/pull/5191) by [@BilalAlpaslan](https://github.com/BilalAlpaslan).
* 🌐 Add Turkish translation for `docs/tr/docs/project-generation.md`. PR [#5192](https://github.com/tiangolo/fastapi/pull/5192) by [@BilalAlpaslan](https://github.com/BilalAlpaslan).
* 🌐 Add Korean translation for `docs/ko/docs/deployment/docker.md`. PR [#5657](https://github.com/tiangolo/fastapi/pull/5657) by [@nearnear](https://github.com/nearnear).
* 🌐 Add Korean translation for `docs/ko/docs/deployment/server-workers.md`. PR [#4935](https://github.com/tiangolo/fastapi/pull/4935) by [@jujumilk3](https://github.com/jujumilk3).
* 🌐 Add Korean translation for `docs/ko/docs/deployment/index.md`. PR [#4561](https://github.com/tiangolo/fastapi/pull/4561) by [@jujumilk3](https://github.com/jujumilk3).
* 🌐 Add Korean translation for `docs/ko/docs/tutorial/path-operation-configuration.md`. PR [#3639](https://github.com/tiangolo/fastapi/pull/3639) by [@jungsu-kwon](https://github.com/jungsu-kwon).
* 🌐 Modify the description of `zh` - Traditional Chinese. PR [#10889](https://github.com/tiangolo/fastapi/pull/10889) by [@cherinyy](https://github.com/cherinyy).
* 🌐 Add Korean translation for `docs/ko/docs/tutorial/static-files.md`. PR [#2957](https://github.com/tiangolo/fastapi/pull/2957) by [@jeesang7](https://github.com/jeesang7).
* 🌐 Add Korean translation for `docs/ko/docs/tutorial/response-model.md`. PR [#2766](https://github.com/tiangolo/fastapi/pull/2766) by [@hard-coders](https://github.com/hard-coders).
* 🌐 Add Korean translation for `docs/ko/docs/tutorial/body-multiple-params.md`. PR [#2461](https://github.com/tiangolo/fastapi/pull/2461) by [@PandaHun](https://github.com/PandaHun).
* 🌐 Add Korean translation for `docs/ko/docs/tutorial/query-params-str-validations.md`. PR [#2415](https://github.com/tiangolo/fastapi/pull/2415) by [@hard-coders](https://github.com/hard-coders).
* 🌐 Add Korean translation for `docs/ko/docs/python-types.md`. PR [#2267](https://github.com/tiangolo/fastapi/pull/2267) by [@jrim](https://github.com/jrim).
* 🌐 Add Korean translation for `docs/ko/docs/tutorial/body-nested-models.md`. PR [#2506](https://github.com/tiangolo/fastapi/pull/2506) by [@hard-coders](https://github.com/hard-coders).
* 🌐 Add Korean translation for `docs/ko/docs/learn/index.md`. PR [#10977](https://github.com/tiangolo/fastapi/pull/10977) by [@KaniKim](https://github.com/KaniKim).
* 🌐 Initialize translations for Traditional Chinese. PR [#10505](https://github.com/tiangolo/fastapi/pull/10505) by [@hsuanchi](https://github.com/hsuanchi).
* ✏️ Tweak the german translation of `docs/de/docs/tutorial/index.md`. PR [#10962](https://github.com/tiangolo/fastapi/pull/10962) by [@nilslindemann](https://github.com/nilslindemann).
* ✏️ Fix typo error in `docs/ko/docs/tutorial/path-params.md`. PR [#10758](https://github.com/tiangolo/fastapi/pull/10758) by [@2chanhaeng](https://github.com/2chanhaeng).
* 🌐 Add Japanese translation for `docs/ja/docs/tutorial/dependencies/dependencies-with-yield.md`. PR [#1961](https://github.com/tiangolo/fastapi/pull/1961) by [@SwftAlpc](https://github.com/SwftAlpc).
* 🌐 Add Japanese translation for `docs/ja/docs/tutorial/dependencies/dependencies-in-path-operation-decorators.md`. PR [#1960](https://github.com/tiangolo/fastapi/pull/1960) by [@SwftAlpc](https://github.com/SwftAlpc).
* 🌐 Add Japanese translation for `docs/ja/docs/tutorial/dependencies/sub-dependencies.md`. PR [#1959](https://github.com/tiangolo/fastapi/pull/1959) by [@SwftAlpc](https://github.com/SwftAlpc).
* 🌐 Add Japanese translation for `docs/ja/docs/tutorial/background-tasks.md`. PR [#2668](https://github.com/tiangolo/fastapi/pull/2668) by [@tokusumi](https://github.com/tokusumi).
* 🌐 Add Japanese translation for `docs/ja/docs/tutorial/dependencies/index.md` and `docs/ja/docs/tutorial/dependencies/classes-as-dependencies.md`. PR [#1958](https://github.com/tiangolo/fastapi/pull/1958) by [@SwftAlpc](https://github.com/SwftAlpc).
* 🌐 Add Japanese translation for `docs/ja/docs/tutorial/response-model.md`. PR [#1938](https://github.com/tiangolo/fastapi/pull/1938) by [@SwftAlpc](https://github.com/SwftAlpc).
* 🌐 Add Japanese translation for `docs/ja/docs/tutorial/body-multiple-params.md`. PR [#1903](https://github.com/tiangolo/fastapi/pull/1903) by [@SwftAlpc](https://github.com/SwftAlpc).
* 🌐 Add Japanese translation for `docs/ja/docs/tutorial/path-params-numeric-validations.md`. PR [#1902](https://github.com/tiangolo/fastapi/pull/1902) by [@SwftAlpc](https://github.com/SwftAlpc).
* 🌐 Add Japanese translation for `docs/ja/docs/python-types.md`. PR [#1899](https://github.com/tiangolo/fastapi/pull/1899) by [@SwftAlpc](https://github.com/SwftAlpc).
* 🌐 Add Japanese translation for `docs/ja/docs/tutorial/handling-errors.md`. PR [#1953](https://github.com/tiangolo/fastapi/pull/1953) by [@SwftAlpc](https://github.com/SwftAlpc).
* 🌐 Add Japanese translation for `docs/ja/docs/tutorial/response-status-code.md`. PR [#1942](https://github.com/tiangolo/fastapi/pull/1942) by [@SwftAlpc](https://github.com/SwftAlpc).
* 🌐 Add Japanese translation for `docs/ja/docs/tutorial/extra-models.md`. PR [#1941](https://github.com/tiangolo/fastapi/pull/1941) by [@SwftAlpc](https://github.com/SwftAlpc).
* 🌐 Add Japanese translation for `docs/ja/docs/tutorial/schema-extra-example.md`. PR [#1931](https://github.com/tiangolo/fastapi/pull/1931) by [@SwftAlpc](https://github.com/SwftAlpc).
* 🌐 Add Japanese translation for `docs/ja/docs/tutorial/body-nested-models.md`. PR [#1930](https://github.com/tiangolo/fastapi/pull/1930) by [@SwftAlpc](https://github.com/SwftAlpc).
* 🌐 Add Japanese translation for `docs/ja/docs/tutorial/body-fields.md`. PR [#1923](https://github.com/tiangolo/fastapi/pull/1923) by [@SwftAlpc](https://github.com/SwftAlpc).
* 🌐 Add German translation for `docs/de/docs/tutorial/index.md`. PR [#9502](https://github.com/tiangolo/fastapi/pull/9502) by [@fhabers21](https://github.com/fhabers21).
* 🌐 Add German translation for `docs/de/docs/tutorial/background-tasks.md`. PR [#10566](https://github.com/tiangolo/fastapi/pull/10566) by [@nilslindemann](https://github.com/nilslindemann).
* ✏️ Fix typo in `docs/ru/docs/index.md`. PR [#10672](https://github.com/tiangolo/fastapi/pull/10672) by [@Delitel-WEB](https://github.com/Delitel-WEB).
* ✏️ Fix typos in `docs/zh/docs/tutorial/extra-data-types.md`. PR [#10727](https://github.com/tiangolo/fastapi/pull/10727) by [@HiemalBeryl](https://github.com/HiemalBeryl).
* 🌐 Add Russian translation for `docs/ru/docs/tutorial/dependencies/classes-as-dependencies.md`. PR [#10410](https://github.com/tiangolo/fastapi/pull/10410) by [@AlertRED](https://github.com/AlertRED).

### Internal

* 👥 Update FastAPI People. PR [#11074](https://github.com/tiangolo/fastapi/pull/11074) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Update sponsors: add Coherence. PR [#11066](https://github.com/tiangolo/fastapi/pull/11066) by [@tiangolo](https://github.com/tiangolo).
* 👷 Upgrade GitHub Action issue-manager. PR [#11056](https://github.com/tiangolo/fastapi/pull/11056) by [@tiangolo](https://github.com/tiangolo).
* 🍱 Update sponsors: TalkPython badge. PR [#11052](https://github.com/tiangolo/fastapi/pull/11052) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Update sponsors: TalkPython badge image. PR [#11048](https://github.com/tiangolo/fastapi/pull/11048) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Update sponsors, remove Deta. PR [#11041](https://github.com/tiangolo/fastapi/pull/11041) by [@tiangolo](https://github.com/tiangolo).
* 💄 Fix CSS breaking RTL languages (erroneously introduced by a previous RTL PR). PR [#11039](https://github.com/tiangolo/fastapi/pull/11039) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Add Italian to `mkdocs.yml`. PR [#11016](https://github.com/tiangolo/fastapi/pull/11016) by [@alejsdev](https://github.com/alejsdev).
* 🔨 Verify `mkdocs.yml` languages in CI, update `docs.py`. PR [#11009](https://github.com/tiangolo/fastapi/pull/11009) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Update config in `label-approved.yml` to accept translations with 1 reviewer. PR [#11007](https://github.com/tiangolo/fastapi/pull/11007) by [@alejsdev](https://github.com/alejsdev).
* 👷 Add changes-requested handling in GitHub Action issue manager. PR [#10971](https://github.com/tiangolo/fastapi/pull/10971) by [@tiangolo](https://github.com/tiangolo).
* 🔧  Group dependencies on dependabot updates. PR [#10952](https://github.com/tiangolo/fastapi/pull/10952) by [@Kludex](https://github.com/Kludex).
* ⬆ Bump actions/setup-python from 4 to 5. PR [#10764](https://github.com/tiangolo/fastapi/pull/10764) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump pypa/gh-action-pypi-publish from 1.8.10 to 1.8.11. PR [#10731](https://github.com/tiangolo/fastapi/pull/10731) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump dawidd6/action-download-artifact from 2.28.0 to 3.0.0. PR [#10777](https://github.com/tiangolo/fastapi/pull/10777) by [@dependabot[bot]](https://github.com/apps/dependabot).
* 🔧  Add support for translations to languages with a longer code name, like `zh-hant`. PR [#10950](https://github.com/tiangolo/fastapi/pull/10950) by [@tiangolo](https://github.com/tiangolo).

## 0.109.0 (2024-01-11)

### Features

* ✨ Add support for Python 3.12. PR [#10666](https://github.com/tiangolo/fastapi/pull/10666) by [@Jamim](https://github.com/Jamim).

### Upgrades

* ⬆️ Upgrade Starlette to >=0.35.0,=0.29.0,=3.7.1,> dep: Start request
    Note over dep: Run code up to yield
    opt raise
        dep -->> handler: Raise HTTPException
        handler -->> client: HTTP error response
        dep -->> dep: Raise other exception
    end
    dep ->> operation: Run dependency, e.g. DB session
    opt raise
        operation -->> dep: Raise HTTPException
        dep -->> handler: Auto forward exception
        handler -->> client: HTTP error response
        operation -->> dep: Raise other exception
        dep -->> handler: Auto forward exception
    end
    operation ->> client: Return response to client
    Note over client,operation: Response is already sent, can't change it anymore
    opt Tasks
        operation -->> tasks: Send background tasks
    end
    opt Raise other exception
        tasks -->> dep: Raise other exception
    end
    Note over dep: After yield
    opt Handle other exception
        dep -->> dep: Handle exception, can't change response. E.g. close DB session.
    end
```

The new execution flow can be found in the docs: [Execution of dependencies with `yield`](https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/#execution-of-dependencies-with-yield).

### Features

* ✨ Add support for raising exceptions (including `HTTPException`) in dependencies with `yield` in the exit code, do not support them in background tasks. PR [#10831](https://github.com/tiangolo/fastapi/pull/10831) by [@tiangolo](https://github.com/tiangolo).

### Internal

* 👥 Update FastAPI People. PR [#10567](https://github.com/tiangolo/fastapi/pull/10567) by [@tiangolo](https://github.com/tiangolo).

## 0.105.0 (2023-12-12)

### Features

* ✨ Add support for multiple Annotated annotations, e.g. `Annotated[str, Field(), Query()]`. PR [#10773](https://github.com/tiangolo/fastapi/pull/10773) by [@tiangolo](https://github.com/tiangolo).

### Refactors

* 🔥 Remove unused NoneType. PR [#10774](https://github.com/tiangolo/fastapi/pull/10774) by [@tiangolo](https://github.com/tiangolo).

### Docs

* 📝 Tweak default suggested configs for generating clients. PR [#10736](https://github.com/tiangolo/fastapi/pull/10736) by [@tiangolo](https://github.com/tiangolo).

### Internal

* 🔧 Update sponsors, add Scalar. PR [#10728](https://github.com/tiangolo/fastapi/pull/10728) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Update sponsors, add PropelAuth. PR [#10760](https://github.com/tiangolo/fastapi/pull/10760) by [@tiangolo](https://github.com/tiangolo).
* 👷 Update build docs, verify README on CI. PR [#10750](https://github.com/tiangolo/fastapi/pull/10750) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Update sponsors, remove Fern. PR [#10729](https://github.com/tiangolo/fastapi/pull/10729) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Update sponsors, add Codacy. PR [#10677](https://github.com/tiangolo/fastapi/pull/10677) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Update sponsors, add Reflex. PR [#10676](https://github.com/tiangolo/fastapi/pull/10676) by [@tiangolo](https://github.com/tiangolo).
* 📝 Update release notes, move and check latest-changes. PR [#10588](https://github.com/tiangolo/fastapi/pull/10588) by [@tiangolo](https://github.com/tiangolo).
* 👷 Upgrade latest-changes GitHub Action. PR [#10587](https://github.com/tiangolo/fastapi/pull/10587) by [@tiangolo](https://github.com/tiangolo).

## 0.104.1 (2023-10-30)

### Fixes

* 📌 Pin Swagger UI version to 5.9.0 temporarily to handle a bug crashing it in 5.9.1. PR [#10529](https://github.com/tiangolo/fastapi/pull/10529) by [@alejandraklachquin](https://github.com/alejandraklachquin).
    * This is not really a bug in FastAPI but in Swagger UI, nevertheless pinning the version will work while a solution is found on the [Swagger UI side](https://github.com/swagger-api/swagger-ui/issues/9337).

### Docs

* 📝 Update data structure and render for external-links. PR [#10495](https://github.com/tiangolo/fastapi/pull/10495) by [@tiangolo](https://github.com/tiangolo).
* ✏️ Fix link to SPDX license identifier in `docs/en/docs/tutorial/metadata.md`. PR [#10433](https://github.com/tiangolo/fastapi/pull/10433) by [@worldworm](https://github.com/worldworm).
* 📝 Update example validation error from Pydantic v1 to match Pydantic v2 in `docs/en/docs/tutorial/path-params.md`. PR [#10043](https://github.com/tiangolo/fastapi/pull/10043) by [@giuliowaitforitdavide](https://github.com/giuliowaitforitdavide).
* ✏️ Fix typos in emoji docs and in some source examples. PR [#10438](https://github.com/tiangolo/fastapi/pull/10438) by [@afuetterer](https://github.com/afuetterer).
* ✏️ Fix typo in `docs/en/docs/reference/dependencies.md`. PR [#10465](https://github.com/tiangolo/fastapi/pull/10465) by [@suravshresth](https://github.com/suravshresth).
* ✏️ Fix typos and rewordings in `docs/en/docs/tutorial/body-nested-models.md`. PR [#10468](https://github.com/tiangolo/fastapi/pull/10468) by [@yogabonito](https://github.com/yogabonito).
* 📝 Update docs, remove references to removed `pydantic.Required` in `docs/en/docs/tutorial/query-params-str-validations.md`. PR [#10469](https://github.com/tiangolo/fastapi/pull/10469) by [@yogabonito](https://github.com/yogabonito).
* ✏️ Fix typo in `docs/en/docs/reference/index.md`. PR [#10467](https://github.com/tiangolo/fastapi/pull/10467) by [@tarsil](https://github.com/tarsil).
* 🔥 Remove unnecessary duplicated docstrings. PR [#10484](https://github.com/tiangolo/fastapi/pull/10484) by [@tiangolo](https://github.com/tiangolo).

### Internal

* ✏️ Update Pydantic links to dotenv support. PR [#10511](https://github.com/tiangolo/fastapi/pull/10511) by [@White-Mask](https://github.com/White-Mask).
* ✏️ Update links in `docs/en/docs/async.md` and `docs/zh/docs/async.md` to make them relative. PR [#10498](https://github.com/tiangolo/fastapi/pull/10498) by [@hasnatsajid](https://github.com/hasnatsajid).
* ✏️ Fix links in `docs/em/docs/async.md`. PR [#10507](https://github.com/tiangolo/fastapi/pull/10507) by [@hasnatsajid](https://github.com/hasnatsajid).
* ✏️ Fix typo in `docs/em/docs/index.md`, Python 3.8. PR [#10521](https://github.com/tiangolo/fastapi/pull/10521) by [@kerriop](https://github.com/kerriop).
* ⬆ Bump pillow from 9.5.0 to 10.1.0. PR [#10446](https://github.com/tiangolo/fastapi/pull/10446) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Update mkdocs-material requirement from =8.1.4 to >=8.1.4,=0.23.0 to >=0.23.0, `Annotated` in `docs/en/docs/tutorial/query-params-str-validations.md`. PR [#9625](https://github.com/tiangolo/fastapi/pull/9625) by [@mccricardo](https://github.com/mccricardo).
* 📝 Use in memory database for testing SQL in docs. PR [#1223](https://github.com/tiangolo/fastapi/pull/1223) by [@HarshaLaxman](https://github.com/HarshaLaxman).

### Translations

* 🌐 Add Russian translation for `docs/ru/docs/tutorial/metadata.md`. PR [#9681](https://github.com/tiangolo/fastapi/pull/9681) by [@TabarakoAkula](https://github.com/TabarakoAkula).
* 🌐 Fix typo in Spanish translation for `docs/es/docs/tutorial/first-steps.md`. PR [#9571](https://github.com/tiangolo/fastapi/pull/9571) by [@lilidl-nft](https://github.com/lilidl-nft).
* 🌐 Add Russian translation for `docs/tutorial/path-operation-configuration.md`. PR [#9696](https://github.com/tiangolo/fastapi/pull/9696) by [@TabarakoAkula](https://github.com/TabarakoAkula).
* 🌐 Add Chinese translation for `docs/zh/docs/advanced/security/index.md`. PR [#9666](https://github.com/tiangolo/fastapi/pull/9666) by [@lordqyxz](https://github.com/lordqyxz).
* 🌐 Add Chinese translations for `docs/zh/docs/advanced/settings.md`. PR [#9652](https://github.com/tiangolo/fastapi/pull/9652) by [@ChoyeonChern](https://github.com/ChoyeonChern).
* 🌐 Add Chinese translations for `docs/zh/docs/advanced/websockets.md`. PR [#9651](https://github.com/tiangolo/fastapi/pull/9651) by [@ChoyeonChern](https://github.com/ChoyeonChern).
* 🌐 Add Chinese translation for `docs/zh/docs/tutorial/testing.md`. PR [#9641](https://github.com/tiangolo/fastapi/pull/9641) by [@wdh99](https://github.com/wdh99).
* 🌐 Add Russian translation for `docs/tutorial/extra-models.md`. PR [#9619](https://github.com/tiangolo/fastapi/pull/9619) by [@ivan-abc](https://github.com/ivan-abc).
* 🌐 Add Russian translation for `docs/tutorial/cors.md`. PR [#9608](https://github.com/tiangolo/fastapi/pull/9608) by [@ivan-abc](https://github.com/ivan-abc).
* 🌐 Add Polish translation for `docs/pl/docs/features.md`. PR [#5348](https://github.com/tiangolo/fastapi/pull/5348) by [@mbroton](https://github.com/mbroton).
* 🌐 Add Russian translation for `docs/ru/docs/tutorial/body-nested-models.md`. PR [#9605](https://github.com/tiangolo/fastapi/pull/9605) by [@Alexandrhub](https://github.com/Alexandrhub).

### Internal

* ⬆ Bump ruff from 0.0.272 to 0.0.275. PR [#9721](https://github.com/tiangolo/fastapi/pull/9721) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Update uvicorn[standard] requirement from =0.12.0 to >=0.12.0,=2.17.0 to >=2.17.0,=1.7.4. This fixes an issue when trying to use an old version of Pydantic. PR [#9567](https://github.com/tiangolo/fastapi/pull/9567) by [@Kludex](https://github.com/Kludex).

### Refactors

* ♻ Remove `media_type` from `ORJSONResponse` as it's inherited from the parent class. PR [#5805](https://github.com/tiangolo/fastapi/pull/5805) by [@Kludex](https://github.com/Kludex).
* ♻ Instantiate `HTTPException` only when needed, optimization refactor. PR [#5356](https://github.com/tiangolo/fastapi/pull/5356) by [@pawamoy](https://github.com/pawamoy).

### Docs

* 🔥 Remove link to Pydantic's benchmark, as it was removed there. PR [#5811](https://github.com/tiangolo/fastapi/pull/5811) by [@Kludex](https://github.com/Kludex).

### Translations

* 🌐 Fix spelling in Indonesian translation of `docs/id/docs/tutorial/index.md`. PR [#5635](https://github.com/tiangolo/fastapi/pull/5635) by [@purwowd](https://github.com/purwowd).
* 🌐 Add Russian translation for `docs/ru/docs/tutorial/index.md`. PR [#5896](https://github.com/tiangolo/fastapi/pull/5896) by [@Wilidon](https://github.com/Wilidon).
* 🌐 Add Chinese translations for `docs/zh/docs/advanced/response-change-status-code.md` and `docs/zh/docs/advanced/response-headers.md`. PR [#9544](https://github.com/tiangolo/fastapi/pull/9544) by [@ChoyeonChern](https://github.com/ChoyeonChern).
* 🌐 Add Russian translation for `docs/ru/docs/tutorial/schema-extra-example.md`. PR [#9621](https://github.com/tiangolo/fastapi/pull/9621) by [@Alexandrhub](https://github.com/Alexandrhub).

### Internal

* 🔧 Add sponsor Platform.sh. PR [#9650](https://github.com/tiangolo/fastapi/pull/9650) by [@tiangolo](https://github.com/tiangolo).
* 👷 Add custom token to Smokeshow and Preview Docs for download-artifact, to prevent API rate limits. PR [#9646](https://github.com/tiangolo/fastapi/pull/9646) by [@tiangolo](https://github.com/tiangolo).
* 👷 Add custom tokens for GitHub Actions to avoid rate limits. PR [#9647](https://github.com/tiangolo/fastapi/pull/9647) by [@tiangolo](https://github.com/tiangolo).

## 0.96.0 (2023-06-03)

### Features

* ⚡ Update `create_cloned_field` to use a global cache and improve startup performance. PR [#4645](https://github.com/tiangolo/fastapi/pull/4645) by [@madkinsz](https://github.com/madkinsz) and previous original PR by [@huonw](https://github.com/huonw).

### Docs

* 📝 Update Deta deployment tutorial for compatibility with Deta Space. PR [#6004](https://github.com/tiangolo/fastapi/pull/6004) by [@mikBighne98](https://github.com/mikBighne98).
* ✏️ Fix typo in Deta deployment tutorial. PR [#9501](https://github.com/tiangolo/fastapi/pull/9501) by [@lemonyte](https://github.com/lemonyte).

### Translations

* 🌐 Add Russian translation for `docs/tutorial/body.md`. PR [#3885](https://github.com/tiangolo/fastapi/pull/3885) by [@solomein-sv](https://github.com/solomein-sv).
* 🌐 Add Russian translation for `docs/ru/docs/tutorial/static-files.md`. PR [#9580](https://github.com/tiangolo/fastapi/pull/9580) by [@Alexandrhub](https://github.com/Alexandrhub).
* 🌐 Add Russian translation for `docs/ru/docs/tutorial/query-params.md`. PR [#9584](https://github.com/tiangolo/fastapi/pull/9584) by [@Alexandrhub](https://github.com/Alexandrhub).
* 🌐 Add Russian translation for `docs/ru/docs/tutorial/first-steps.md`. PR [#9471](https://github.com/tiangolo/fastapi/pull/9471) by [@AGolicyn](https://github.com/AGolicyn).
* 🌐 Add Russian translation for `docs/ru/docs/tutorial/debugging.md`. PR [#9579](https://github.com/tiangolo/fastapi/pull/9579) by [@Alexandrhub](https://github.com/Alexandrhub).
* 🌐 Add Russian translation for `docs/ru/docs/tutorial/path-params.md`. PR [#9519](https://github.com/tiangolo/fastapi/pull/9519) by [@AGolicyn](https://github.com/AGolicyn).
* 🌐 Add Chinese translation for `docs/zh/docs/tutorial/static-files.md`. PR [#9436](https://github.com/tiangolo/fastapi/pull/9436) by [@wdh99](https://github.com/wdh99).
* 🌐 Update Spanish translation including new illustrations in `docs/es/docs/async.md`. PR [#9483](https://github.com/tiangolo/fastapi/pull/9483) by [@andresbermeoq](https://github.com/andresbermeoq).
* 🌐 Add Russian translation for `docs/ru/docs/tutorial/path-params-numeric-validations.md`. PR [#9563](https://github.com/tiangolo/fastapi/pull/9563) by [@ivan-abc](https://github.com/ivan-abc).
* 🌐 Add Russian translation for `docs/ru/docs/deployment/concepts.md`. PR [#9577](https://github.com/tiangolo/fastapi/pull/9577) by [@Xewus](https://github.com/Xewus).
* 🌐 Add Russian translation for `docs/ru/docs/tutorial/body-multiple-params.md`. PR [#9586](https://github.com/tiangolo/fastapi/pull/9586) by [@Alexandrhub](https://github.com/Alexandrhub).

### Internal

* 👥 Update FastAPI People. PR [#9602](https://github.com/tiangolo/fastapi/pull/9602) by [@github-actions[bot]](https://github.com/apps/github-actions).
* 🔧 Update sponsors, remove InvestSuite. PR [#9612](https://github.com/tiangolo/fastapi/pull/9612) by [@tiangolo](https://github.com/tiangolo).

## 0.95.2 (2023-05-16)

* ⬆️ Upgrade Starlette version to `>=0.27.0` for a security release. PR [#9541](https://github.com/tiangolo/fastapi/pull/9541) by [@tiangolo](https://github.com/tiangolo). Details on [Starlette's security advisory](https://github.com/encode/starlette/security/advisories/GHSA-v5gw-mw7f-84px).

### Translations

* 🌐 Add Portuguese translation for `docs/pt/docs/advanced/events.md`. PR [#9326](https://github.com/tiangolo/fastapi/pull/9326) by [@oandersonmagalhaes](https://github.com/oandersonmagalhaes).
* 🌐 Add Russian translation for `docs/ru/docs/deployment/manually.md`. PR [#9417](https://github.com/tiangolo/fastapi/pull/9417) by [@Xewus](https://github.com/Xewus).
* 🌐 Add setup for translations to Lao. PR [#9396](https://github.com/tiangolo/fastapi/pull/9396) by [@TheBrown](https://github.com/TheBrown).
* 🌐 Add Russian translation for `docs/ru/docs/tutorial/testing.md`. PR [#9403](https://github.com/tiangolo/fastapi/pull/9403) by [@Xewus](https://github.com/Xewus).
* 🌐 Add Russian translation for `docs/ru/docs/deployment/https.md`. PR [#9428](https://github.com/tiangolo/fastapi/pull/9428) by [@Xewus](https://github.com/Xewus).
* ✏ Fix command to install requirements in Windows. PR [#9445](https://github.com/tiangolo/fastapi/pull/9445) by [@MariiaRomanuik](https://github.com/MariiaRomanuik).
* 🌐 Add French translation for `docs/fr/docs/advanced/response-directly.md`. PR [#9415](https://github.com/tiangolo/fastapi/pull/9415) by [@axel584](https://github.com/axel584).
* 🌐 Initiate Czech translation setup. PR [#9288](https://github.com/tiangolo/fastapi/pull/9288) by [@3p1463k](https://github.com/3p1463k).
* ✏ Fix typo in Portuguese docs for `docs/pt/docs/index.md`. PR [#9337](https://github.com/tiangolo/fastapi/pull/9337) by [@lucasbalieiro](https://github.com/lucasbalieiro).
* 🌐 Add Russian translation for `docs/ru/docs/tutorial/response-status-code.md`. PR [#9370](https://github.com/tiangolo/fastapi/pull/9370) by [@nadia3373](https://github.com/nadia3373).

### Internal

* 🐛 Fix `flask.escape` warning for internal tests. PR [#9468](https://github.com/tiangolo/fastapi/pull/9468) by [@samuelcolvin](https://github.com/samuelcolvin).
* ✅ Refactor 2 tests, for consistency and simplification. PR [#9504](https://github.com/tiangolo/fastapi/pull/9504) by [@tiangolo](https://github.com/tiangolo).
* ✅ Refactor OpenAPI tests, prepare for Pydantic v2. PR [#9503](https://github.com/tiangolo/fastapi/pull/9503) by [@tiangolo](https://github.com/tiangolo).
* ⬆ Bump dawidd6/action-download-artifact from 2.26.0 to 2.27.0. PR [#9394](https://github.com/tiangolo/fastapi/pull/9394) by [@dependabot[bot]](https://github.com/apps/dependabot).
* 💚 Disable setup-python pip cache in CI. PR [#9438](https://github.com/tiangolo/fastapi/pull/9438) by [@tiangolo](https://github.com/tiangolo).
* ⬆ Bump pypa/gh-action-pypi-publish from 1.6.4 to 1.8.5. PR [#9346](https://github.com/tiangolo/fastapi/pull/9346) by [@dependabot[bot]](https://github.com/apps/dependabot).

## 0.95.1 (2023-04-13)

### Fixes

* 🐛 Fix using `Annotated` in routers or path operations decorated multiple times. PR [#9315](https://github.com/tiangolo/fastapi/pull/9315) by [@sharonyogev](https://github.com/sharonyogev).

### Docs

* 🌐 🔠 📄 🐢 Translate docs to Emoji 🥳 🎉 💥 🤯 🤯. PR [#5385](https://github.com/tiangolo/fastapi/pull/5385) by [@LeeeeT](https://github.com/LeeeeT).
* 📝 Add notification message warning about old versions of FastAPI not supporting `Annotated`. PR [#9298](https://github.com/tiangolo/fastapi/pull/9298) by [@grdworkin](https://github.com/grdworkin).
* 📝 Fix typo in `docs/en/docs/advanced/behind-a-proxy.md`. PR [#5681](https://github.com/tiangolo/fastapi/pull/5681) by [@Leommjr](https://github.com/Leommjr).
* ✏ Fix wrong import from typing module in Persian translations for `docs/fa/docs/index.md`. PR [#6083](https://github.com/tiangolo/fastapi/pull/6083) by [@Kimiaattaei](https://github.com/Kimiaattaei).
* ✏️ Fix format, remove unnecessary asterisks in `docs/en/docs/help-fastapi.md`. PR [#9249](https://github.com/tiangolo/fastapi/pull/9249) by [@armgabrielyan](https://github.com/armgabrielyan).
* ✏ Fix typo in `docs/en/docs/tutorial/query-params-str-validations.md`. PR [#9272](https://github.com/tiangolo/fastapi/pull/9272) by [@nicornk](https://github.com/nicornk).
* ✏ Fix typo/bug in inline code example in `docs/en/docs/tutorial/query-params-str-validations.md`. PR [#9273](https://github.com/tiangolo/fastapi/pull/9273) by [@tim-habitat](https://github.com/tim-habitat).
* ✏ Fix typo in `docs/en/docs/tutorial/path-params-numeric-validations.md`. PR [#9282](https://github.com/tiangolo/fastapi/pull/9282) by [@aadarsh977](https://github.com/aadarsh977).
* ✏ Fix typo: 'wll' to 'will' in `docs/en/docs/tutorial/query-params-str-validations.md`. PR [#9380](https://github.com/tiangolo/fastapi/pull/9380) by [@dasstyxx](https://github.com/dasstyxx).

### Translations

* 🌐 Add French translation for `docs/fr/docs/advanced/index.md`. PR [#5673](https://github.com/tiangolo/fastapi/pull/5673) by [@axel584](https://github.com/axel584).
* 🌐 Add Portuguese translation for `docs/pt/docs/tutorial/body-nested-models.md`. PR [#4053](https://github.com/tiangolo/fastapi/pull/4053) by [@luccasmmg](https://github.com/luccasmmg).
* 🌐 Add Russian translation for `docs/ru/docs/alternatives.md`. PR [#5994](https://github.com/tiangolo/fastapi/pull/5994) by [@Xewus](https://github.com/Xewus).
* 🌐 Add Portuguese translation for `docs/pt/docs/tutorial/extra-models.md`. PR [#5912](https://github.com/tiangolo/fastapi/pull/5912) by [@LorhanSohaky](https://github.com/LorhanSohaky).
* 🌐 Add Portuguese translation for `docs/pt/docs/tutorial/path-operation-configuration.md`. PR [#5936](https://github.com/tiangolo/fastapi/pull/5936) by [@LorhanSohaky](https://github.com/LorhanSohaky).
* 🌐 Add Russian translation for `docs/ru/docs/contributing.md`. PR [#6002](https://github.com/tiangolo/fastapi/pull/6002) by [@stigsanek](https://github.com/stigsanek).
* 🌐 Add Korean translation for `docs/tutorial/dependencies/classes-as-dependencies.md`. PR [#9176](https://github.com/tiangolo/fastapi/pull/9176) by [@sehwan505](https://github.com/sehwan505).
* 🌐 Add Russian translation for `docs/ru/docs/project-generation.md`. PR [#9243](https://github.com/tiangolo/fastapi/pull/9243) by [@Xewus](https://github.com/Xewus).
* 🌐 Add French translation for `docs/fr/docs/index.md`. PR [#9265](https://github.com/tiangolo/fastapi/pull/9265) by [@frabc](https://github.com/frabc).
* 🌐 Add Russian translation for `docs/ru/docs/tutorial/query-params-str-validations.md`. PR [#9267](https://github.com/tiangolo/fastapi/pull/9267) by [@dedkot01](https://github.com/dedkot01).
* 🌐 Add Russian translation for `docs/ru/docs/benchmarks.md`. PR [#9271](https://github.com/tiangolo/fastapi/pull/9271) by [@Xewus](https://github.com/Xewus).

### Internal

* 🔧 Update sponsors: remove Jina. PR [#9388](https://github.com/tiangolo/fastapi/pull/9388) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Update sponsors, add databento, remove Ines's course and StriveWorks. PR [#9351](https://github.com/tiangolo/fastapi/pull/9351) by [@tiangolo](https://github.com/tiangolo).

## 0.95.0 (2023-03-18)

### Highlights

This release adds support for dependencies and parameters using `Annotated` and recommends its usage. ✨

This has **several benefits**, one of the main ones is that now the parameters of your functions with `Annotated` would **not be affected** at all.

If you call those functions in **other places in your code**, the actual **default values** will be kept, your editor will help you notice missing **required arguments**, Python will require you to pass required arguments at **runtime**, you will be able to **use the same functions** for different things and with different libraries (e.g. **Typer** will soon support `Annotated` too, then you could use the same function for an API and a CLI), etc.

Because `Annotated` is **standard Python**, you still get all the **benefits** from editors and tools, like **autocompletion**, **inline errors**, etc.

One of the **biggest benefits** is that now you can create `Annotated` dependencies that are then shared by multiple *path operation functions*, this will allow you to **reduce** a lot of **code duplication** in your codebase, while keeping all the support from editors and tools.

For example, you could have code like this:

```Python
def get_current_user(token: str):
    # authenticate user
    return User()

@app.get("/items/")
def read_items(user: User = Depends(get_current_user)):
    ...

@app.post("/items/")
def create_item(*, user: User = Depends(get_current_user), item: Item):
    ...

@app.get("/items/{item_id}")
def read_item(*, user: User = Depends(get_current_user), item_id: int):
    ...

@app.delete("/items/{item_id}")
def delete_item(*, user: User = Depends(get_current_user), item_id: int):
    ...
```

There's a bit of code duplication for the dependency:

```Python
user: User = Depends(get_current_user)
```

...the bigger the codebase, the more noticeable it is.

Now you can create an annotated dependency once, like this:

```Python
CurrentUser = Annotated[User, Depends(get_current_user)]
```

And then you can reuse this `Annotated` dependency:

```Python
CurrentUser = Annotated[User, Depends(get_current_user)]

@app.get("/items/")
def read_items(user: CurrentUser):
    ...

@app.post("/items/")
def create_item(user: CurrentUser, item: Item):
    ...

@app.get("/items/{item_id}")
def read_item(user: CurrentUser, item_id: int):
    ...

@app.delete("/items/{item_id}")
def delete_item(user: CurrentUser, item_id: int):
    ...
```

...and `CurrentUser` has all the typing information as `User`, so your editor will work as expected (autocompletion and everything), and **FastAPI** will be able to understand the dependency defined in `Annotated`. 😎

Roughly **all the docs** have been rewritten to use `Annotated` as the main way to declare **parameters** and **dependencies**. All the **examples** in the docs now include a version with `Annotated` and a version without it, for each of the specific Python versions (when there are small differences/improvements in more recent versions). There were around 23K new lines added between docs, examples, and tests. 🚀

The key updated docs are:

* Python Types Intro:
    * [Type Hints with Metadata Annotations](https://fastapi.tiangolo.com/python-types/#type-hints-with-metadata-annotations).
* Tutorial:
    * [Query Parameters and String Validations - Additional validation](https://fastapi.tiangolo.com/tutorial/query-params-str-validations/#additional-validation)
        * [Advantages of `Annotated`](https://fastapi.tiangolo.com/tutorial/query-params-str-validations/#advantages-of-annotated)
    * [Path Parameters and Numeric Validations - Order the parameters as you need, tricks](https://fastapi.tiangolo.com/tutorial/path-params-numeric-validations/#order-the-parameters-as-you-need-tricks)
        * [Better with `Annotated`](https://fastapi.tiangolo.com/tutorial/path-params-numeric-validations/#better-with-annotated)
    * [Dependencies - First Steps - Share `Annotated` dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/#share-annotated-dependencies)

Special thanks to [@nzig](https://github.com/nzig) for the core implementation and to [@adriangb](https://github.com/adriangb) for the inspiration and idea with [Xpresso](https://github.com/adriangb/xpresso)! 🚀

### Features

* ✨Add support for PEP-593 `Annotated` for specifying dependencies and parameters. PR [#4871](https://github.com/tiangolo/fastapi/pull/4871) by [@nzig](https://github.com/nzig).

### Docs

* 📝 Tweak tip recommending `Annotated` in docs. PR [#9270](https://github.com/tiangolo/fastapi/pull/9270) by [@tiangolo](https://github.com/tiangolo).
* 📝 Update order of examples, latest Python version first, and simplify version tab names. PR [#9269](https://github.com/tiangolo/fastapi/pull/9269) by [@tiangolo](https://github.com/tiangolo).
* 📝 Update all docs to use `Annotated` as the main recommendation, with new examples and tests. PR [#9268](https://github.com/tiangolo/fastapi/pull/9268) by [@tiangolo](https://github.com/tiangolo).

## 0.94.1 (2023-03-14)

### Fixes

* 🎨 Fix types for lifespan, upgrade Starlette to 0.26.1. PR [#9245](https://github.com/tiangolo/fastapi/pull/9245) by [@tiangolo](https://github.com/tiangolo).

## 0.94.0 (2023-03-10)

### Upgrades

* ⬆ Upgrade python-multipart to support 0.0.6. PR [#9212](https://github.com/tiangolo/fastapi/pull/9212) by [@musicinmybrain](https://github.com/musicinmybrain).
* ⬆️ Upgrade Starlette version, support new `lifespan` with state. PR [#9239](https://github.com/tiangolo/fastapi/pull/9239) by [@tiangolo](https://github.com/tiangolo).

### Docs

* 📝 Update Sentry link in docs. PR [#9218](https://github.com/tiangolo/fastapi/pull/9218) by [@smeubank](https://github.com/smeubank).

### Translations

* 🌐 Add Russian translation for `docs/ru/docs/history-design-future.md`. PR [#5986](https://github.com/tiangolo/fastapi/pull/5986) by [@Xewus](https://github.com/Xewus).

### Internal

* ➕ Add `pydantic` to PyPI classifiers. PR [#5914](https://github.com/tiangolo/fastapi/pull/5914) by [@yezz123](https://github.com/yezz123).
* ⬆ Bump black from 22.10.0 to 23.1.0. PR [#5953](https://github.com/tiangolo/fastapi/pull/5953) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump types-ujson from 5.6.0.0 to 5.7.0.1. PR [#6027](https://github.com/tiangolo/fastapi/pull/6027) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ Bump dawidd6/action-download-artifact from 2.24.3 to 2.26.0. PR [#6034](https://github.com/tiangolo/fastapi/pull/6034) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ [pre-commit.ci] pre-commit autoupdate. PR [#5709](https://github.com/tiangolo/fastapi/pull/5709) by [@pre-commit-ci[bot]](https://github.com/apps/pre-commit-ci).

## 0.93.0 (2023-03-07)

### Features

* ✨ Add support for `lifespan` async context managers (superseding `startup` and `shutdown` events). Initial PR [#2944](https://github.com/tiangolo/fastapi/pull/2944) by [@uSpike](https://github.com/uSpike).

Now, instead of using independent `startup` and `shutdown` events, you can define that logic in a single function with `yield` decorated with `@asynccontextmanager` (an async context manager).

For example:

```Python
from contextlib import asynccontextmanager

from fastapi import FastAPI

def fake_answer_to_everything_ml_model(x: float):
    return x * 42

ml_models = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    ml_models["answer_to_everything"] = fake_answer_to_everything_ml_model
    yield
    # Clean up the ML models and release the resources
    ml_models.clear()

app = FastAPI(lifespan=lifespan)

@app.get("/predict")
async def predict(x: float):
    result = ml_models["answer_to_everything"](x)
    return {"result": result}
```

**Note**: This is the recommended way going forward, instead of using `startup` and `shutdown` events.

Read more about it in the new docs: [Advanced User Guide: Lifespan Events](https://fastapi.tiangolo.com/advanced/events/).

### Docs

* ✏ Fix formatting in `docs/en/docs/tutorial/metadata.md` for `ReDoc`. PR [#6005](https://github.com/tiangolo/fastapi/pull/6005) by [@eykamp](https://github.com/eykamp).

### Translations

* 🌐 Tamil translations - initial setup. PR [#5564](https://github.com/tiangolo/fastapi/pull/5564) by [@gusty1g](https://github.com/gusty1g).
* 🌐 Add French translation for `docs/fr/docs/advanced/path-operation-advanced-configuration.md`. PR [#9221](https://github.com/tiangolo/fastapi/pull/9221) by [@axel584](https://github.com/axel584).
* 🌐 Add French translation for `docs/tutorial/debugging.md`. PR [#9175](https://github.com/tiangolo/fastapi/pull/9175) by [@frabc](https://github.com/frabc).
* 🌐 Initiate Armenian translation setup. PR [#5844](https://github.com/tiangolo/fastapi/pull/5844) by [@har8](https://github.com/har8).
* 🌐 Add French translation for `deployment/manually.md`. PR [#3693](https://github.com/tiangolo/fastapi/pull/3693) by [@rjNemo](https://github.com/rjNemo).

### Internal

* 👷 Update translation bot messages. PR [#9206](https://github.com/tiangolo/fastapi/pull/9206) by [@tiangolo](https://github.com/tiangolo).
* 👷 Update translations bot to use Discussions, and notify when a PR is done. PR [#9183](https://github.com/tiangolo/fastapi/pull/9183) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Update sponsors-badges. PR [#9182](https://github.com/tiangolo/fastapi/pull/9182) by [@tiangolo](https://github.com/tiangolo).
* 👥 Update FastAPI People. PR [#9181](https://github.com/tiangolo/fastapi/pull/9181) by [@github-actions[bot]](https://github.com/apps/github-actions).
* 🔊 Log GraphQL errors in FastAPI People, because it returns 200, with a payload with an error. PR [#9171](https://github.com/tiangolo/fastapi/pull/9171) by [@tiangolo](https://github.com/tiangolo).
* 💚 Fix/workaround GitHub Actions in Docker with git for FastAPI People. PR [#9169](https://github.com/tiangolo/fastapi/pull/9169) by [@tiangolo](https://github.com/tiangolo).
* ♻️ Refactor FastAPI Experts to use only discussions now that questions are migrated. PR [#9165](https://github.com/tiangolo/fastapi/pull/9165) by [@tiangolo](https://github.com/tiangolo).
* ⬆️ Upgrade analytics. PR [#6025](https://github.com/tiangolo/fastapi/pull/6025) by [@tiangolo](https://github.com/tiangolo).
* ⬆️ Upgrade and re-enable installing Typer-CLI. PR [#6008](https://github.com/tiangolo/fastapi/pull/6008) by [@tiangolo](https://github.com/tiangolo).

## 0.92.0 (2023-02-14)

🚨 This is a security fix. Please upgrade as soon as possible.

### Upgrades

* ⬆️ Upgrade Starlette to 0.25.0. PR [#5996](https://github.com/tiangolo/fastapi/pull/5996) by [@tiangolo](https://github.com/tiangolo).
    * This solves a vulnerability that could allow denial of service attacks by using many small multipart fields/files (parts), consuming high CPU and memory.
    * Only applications using forms (e.g. file uploads) could be affected.
    * For most cases, upgrading won't have any breaking changes.

## 0.91.0 (2023-02-10)

### Upgrades

* ⬆️ Upgrade Starlette version to `0.24.0` and refactor internals for compatibility. PR [#5985](https://github.com/tiangolo/fastapi/pull/5985) by [@tiangolo](https://github.com/tiangolo).
    * This can solve nuanced errors when using middlewares. Before Starlette `0.24.0`, a new instance of each middleware class would be created when a new middleware was added. That normally was not a problem, unless the middleware class expected to be created only once, with only one instance, that happened in some cases. This upgrade would solve those cases (thanks [@adriangb](https://github.com/adriangb)! Starlette PR [#2017](https://github.com/encode/starlette/pull/2017)). Now the middleware class instances are created once, right before the first request (the first time the app is called).
    * If you depended on that previous behavior, you might need to update your code. As always, make sure your tests pass before merging the upgrade.

## 0.90.1 (2023-02-09)

### Upgrades

* ⬆️ Upgrade Starlette range to allow 0.23.1. PR [#5980](https://github.com/tiangolo/fastapi/pull/5980) by [@tiangolo](https://github.com/tiangolo).

### Docs

* ✏ Tweak wording to clarify `docs/en/docs/project-generation.md`. PR [#5930](https://github.com/tiangolo/fastapi/pull/5930) by [@chandra-deb](https://github.com/chandra-deb).
* ✏ Update Pydantic GitHub URLs. PR [#5952](https://github.com/tiangolo/fastapi/pull/5952) by [@yezz123](https://github.com/yezz123).
* 📝 Add opinion from Cisco. PR [#5981](https://github.com/tiangolo/fastapi/pull/5981) by [@tiangolo](https://github.com/tiangolo).

### Translations

* 🌐 Add Russian translation for `docs/ru/docs/tutorial/cookie-params.md`. PR [#5890](https://github.com/tiangolo/fastapi/pull/5890) by [@bnzone](https://github.com/bnzone).

### Internal

* ✏ Update `zip-docs.sh` internal script, remove extra space. PR [#5931](https://github.com/tiangolo/fastapi/pull/5931) by [@JuanPerdomo00](https://github.com/JuanPerdomo00).

## 0.90.0 (2023-02-08)

### Upgrades

* ⬆️ Bump Starlette from 0.22.0 to 0.23.0. Initial PR [#5739](https://github.com/tiangolo/fastapi/pull/5739) by [@Kludex](https://github.com/Kludex).

### Docs

* 📝 Add article "Tortoise ORM / FastAPI 整合快速筆記" to External Links. PR [#5496](https://github.com/tiangolo/fastapi/pull/5496) by [@Leon0824](https://github.com/Leon0824).
* 👥 Update FastAPI People. PR [#5954](https://github.com/tiangolo/fastapi/pull/5954) by [@github-actions[bot]](https://github.com/apps/github-actions).
* 📝 Micro-tweak help docs. PR [#5960](https://github.com/tiangolo/fastapi/pull/5960) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Update new issue chooser to direct to GitHub Discussions. PR [#5948](https://github.com/tiangolo/fastapi/pull/5948) by [@tiangolo](https://github.com/tiangolo).
* 📝 Recommend GitHub Discussions for questions. PR [#5944](https://github.com/tiangolo/fastapi/pull/5944) by [@tiangolo](https://github.com/tiangolo).

### Translations

* 🌐 Add Russian translation for `docs/ru/docs/tutorial/body-fields.md`. PR [#5898](https://github.com/tiangolo/fastapi/pull/5898) by [@simatheone](https://github.com/simatheone).
* 🌐 Add Russian translation for `docs/ru/docs/help-fastapi.md`. PR [#5970](https://github.com/tiangolo/fastapi/pull/5970) by [@tiangolo](https://github.com/tiangolo).
* 🌐 Add Portuguese translation for `docs/pt/docs/tutorial/static-files.md`. PR [#5858](https://github.com/tiangolo/fastapi/pull/5858) by [@batlopes](https://github.com/batlopes).
* 🌐 Add Portuguese translation for `docs/pt/docs/tutorial/encoder.md`. PR [#5525](https://github.com/tiangolo/fastapi/pull/5525) by [@felipebpl](https://github.com/felipebpl).
* 🌐 Add Russian translation for `docs/ru/docs/contributing.md`. PR [#5870](https://github.com/tiangolo/fastapi/pull/5870) by [@Xewus](https://github.com/Xewus).

### Internal

* ⬆️ Upgrade Ubuntu version for docs workflow. PR [#5971](https://github.com/tiangolo/fastapi/pull/5971) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Update sponsors badges. PR [#5943](https://github.com/tiangolo/fastapi/pull/5943) by [@tiangolo](https://github.com/tiangolo).
* ✨ Compute FastAPI Experts including GitHub Discussions. PR [#5941](https://github.com/tiangolo/fastapi/pull/5941) by [@tiangolo](https://github.com/tiangolo).
* ⬆️ Upgrade isort and update pre-commit. PR [#5940](https://github.com/tiangolo/fastapi/pull/5940) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Add template for questions in Discussions. PR [#5920](https://github.com/tiangolo/fastapi/pull/5920) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Update Sponsor Budget Insight to Powens. PR [#5916](https://github.com/tiangolo/fastapi/pull/5916) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Update GitHub Sponsors badge data. PR [#5915](https://github.com/tiangolo/fastapi/pull/5915) by [@tiangolo](https://github.com/tiangolo).

## 0.89.1 (2023-01-10)

### Fixes

* 🐛 Ignore Response classes on return annotation. PR [#5855](https://github.com/tiangolo/fastapi/pull/5855) by [@Kludex](https://github.com/Kludex). See the new docs in the PR below.

### Docs

* 📝 Update docs and examples for Response Model with Return Type Annotations, and update runtime error. PR [#5873](https://github.com/tiangolo/fastapi/pull/5873) by [@tiangolo](https://github.com/tiangolo). New docs at [Response Model - Return Type: Other Return Type Annotations](https://fastapi.tiangolo.com/tutorial/response-model/#other-return-type-annotations).
* 📝 Add External Link: FastAPI lambda container: serverless simplified. PR [#5784](https://github.com/tiangolo/fastapi/pull/5784) by [@rafrasenberg](https://github.com/rafrasenberg).

### Translations

* 🌐 Add Turkish translation for `docs/tr/docs/tutorial/first_steps.md`. PR [#5691](https://github.com/tiangolo/fastapi/pull/5691) by [@Kadermiyanyedi](https://github.com/Kadermiyanyedi).

## 0.89.0 (2023-01-07)

### Features

* ✨ Add support for function return type annotations to declare the `response_model`. Initial PR [#1436](https://github.com/tiangolo/fastapi/pull/1436) by [@uriyyo](https://github.com/uriyyo).

Now you can declare the return type / `response_model` in the function return type annotation:

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float

@app.get("/items/")
async def read_items() -> list[Item]:
    return [
        Item(name="Portal Gun", price=42.0),
        Item(name="Plumbus", price=32.0),
    ]
```

FastAPI will use the return type annotation to perform:

* Data validation
* Automatic documentation
    * It could power automatic client generators
* **Data filtering**

Before this version it was only supported via the `response_model` parameter.

Read more about it in the new docs: [Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/).

### Docs

* 📝 Add External Link: Authorization on FastAPI with Casbin. PR [#5712](https://github.com/tiangolo/fastapi/pull/5712) by [@Xhy-5000](https://github.com/Xhy-5000).
* ✏ Fix typo in `docs/en/docs/async.md`. PR [#5785](https://github.com/tiangolo/fastapi/pull/5785) by [@Kingdageek](https://github.com/Kingdageek).
* ✏ Fix typo in `docs/en/docs/deployment/concepts.md`. PR [#5824](https://github.com/tiangolo/fastapi/pull/5824) by [@kelbyfaessler](https://github.com/kelbyfaessler).

### Translations

* 🌐 Add Russian translation for `docs/ru/docs/fastapi-people.md`. PR [#5577](https://github.com/tiangolo/fastapi/pull/5577) by [@Xewus](https://github.com/Xewus).
* 🌐 Fix typo in Chinese translation for `docs/zh/docs/benchmarks.md`. PR [#4269](https://github.com/tiangolo/fastapi/pull/4269) by [@15027668g](https://github.com/15027668g).
* 🌐 Add Korean translation for `docs/tutorial/cors.md`. PR [#3764](https://github.com/tiangolo/fastapi/pull/3764) by [@NinaHwang](https://github.com/NinaHwang).

### Internal

* ⬆ Update coverage[toml] requirement from =6.5.0 to >=6.5.0,=0.12.0 to >=0.12.0,=1.3.18 to >=1.3.18,=0.6.1 to >=0.6.1,=2.12.0 to >=2.12.0,=0.12.0,=0.12.0,` warning when JS is disabled. PR [#5074](https://github.com/tiangolo/fastapi/pull/5074) by [@evroon](https://github.com/evroon).
* ✨ Add support for `FrozenSet` in parameters (e.g. query). PR [#2938](https://github.com/tiangolo/fastapi/pull/2938) by [@juntatalor](https://github.com/juntatalor).
* ✨ Allow custom middlewares to raise `HTTPException`s and propagate them. PR [#2036](https://github.com/tiangolo/fastapi/pull/2036) by [@ghandic](https://github.com/ghandic).
* ✨ Preserve `json.JSONDecodeError` information when handling invalid JSON in request body, to support custom exception handlers that use its information. PR [#4057](https://github.com/tiangolo/fastapi/pull/4057) by [@UKnowWhoIm](https://github.com/UKnowWhoIm).

### Fixes

* 🐛 Fix `jsonable_encoder` for dataclasses with pydantic-compatible fields. PR [#3607](https://github.com/tiangolo/fastapi/pull/3607) by [@himbeles](https://github.com/himbeles).
* 🐛 Fix support for extending `openapi_extras` with parameter lists. PR [#4267](https://github.com/tiangolo/fastapi/pull/4267) by [@orilevari](https://github.com/orilevari).

### Docs

* ✏ Fix a simple typo in `docs/en/docs/python-types.md`. PR [#5193](https://github.com/tiangolo/fastapi/pull/5193) by [@GlitchingCore](https://github.com/GlitchingCore).
* ✏ Fix typos in `tests/test_schema_extra_examples.py`. PR [#5126](https://github.com/tiangolo/fastapi/pull/5126) by [@supraaxdd](https://github.com/supraaxdd).
* ✏ Fix typos in `docs/en/docs/tutorial/path-params-numeric-validations.md`. PR [#5142](https://github.com/tiangolo/fastapi/pull/5142) by [@invisibleroads](https://github.com/invisibleroads).
* 📝 Add step about upgrading pip in the venv to avoid errors when installing dependencies `docs/en/docs/contributing.md`. PR [#5181](https://github.com/tiangolo/fastapi/pull/5181) by [@edisnake](https://github.com/edisnake).
* ✏ Reword and clarify text in tutorial `docs/en/docs/tutorial/body-nested-models.md`. PR [#5169](https://github.com/tiangolo/fastapi/pull/5169) by [@papb](https://github.com/papb).
* ✏ Fix minor typo in `docs/en/docs/features.md`. PR [#5206](https://github.com/tiangolo/fastapi/pull/5206) by [@OtherBarry](https://github.com/OtherBarry).
* ✏ Fix minor typos in `docs/en/docs/async.md`. PR [#5125](https://github.com/tiangolo/fastapi/pull/5125) by [@Ksenofanex](https://github.com/Ksenofanex).
* 📝 Add external link to docs: "Fastapi, Docker(Docker compose) and Postgres". PR [#5033](https://github.com/tiangolo/fastapi/pull/5033) by [@krishnardt](https://github.com/krishnardt).
* 📝 Simplify example for docs for Additional Responses, remove unnecessary `else`. PR [#4693](https://github.com/tiangolo/fastapi/pull/4693) by [@adriangb](https://github.com/adriangb).
* 📝 Update docs, compare enums with identity instead of equality. PR [#4905](https://github.com/tiangolo/fastapi/pull/4905) by [@MicaelJarniac](https://github.com/MicaelJarniac).
* ✏ Fix typo in `docs/en/docs/python-types.md`. PR [#4886](https://github.com/tiangolo/fastapi/pull/4886) by [@MicaelJarniac](https://github.com/MicaelJarniac).
* 🎨 Fix syntax highlighting in docs for OpenAPI Callbacks. PR [#4368](https://github.com/tiangolo/fastapi/pull/4368) by [@xncbf](https://github.com/xncbf).
* ✏ Reword confusing sentence in docs file `typo-fix-path-params-numeric-validations.md`. PR [#3219](https://github.com/tiangolo/fastapi/pull/3219) by [@ccrenfroe](https://github.com/ccrenfroe).
* 📝 Update docs for handling HTTP Basic Auth with `secrets.compare_digest()` to account for non-ASCII characters. PR [#3536](https://github.com/tiangolo/fastapi/pull/3536) by [@lewoudar](https://github.com/lewoudar).
* 📝 Update docs for testing, fix examples with relative imports. PR [#5302](https://github.com/tiangolo/fastapi/pull/5302) by [@tiangolo](https://github.com/tiangolo).

### Translations

* 🌐 Add Russian translation for `docs/ru/docs/index.md`. PR [#5289](https://github.com/tiangolo/fastapi/pull/5289) by [@impocode](https://github.com/impocode).
* 🌐 Add Russian translation for `docs/ru/docs/deployment/versions.md`. PR [#4985](https://github.com/tiangolo/fastapi/pull/4985) by [@emp7yhead](https://github.com/emp7yhead).
* 🌐 Add Portuguese translation for `docs/pt/docs/tutorial/header-params.md`. PR [#4921](https://github.com/tiangolo/fastapi/pull/4921) by [@batlopes](https://github.com/batlopes).
* 🌐 Update `ko/mkdocs.yml` for a missing link. PR [#5020](https://github.com/tiangolo/fastapi/pull/5020) by [@dalinaum](https://github.com/dalinaum).

### Internal

* ⬆ Bump dawidd6/action-download-artifact from 2.21.1 to 2.22.0. PR [#5258](https://github.com/tiangolo/fastapi/pull/5258) by [@dependabot[bot]](https://github.com/apps/dependabot).
* ⬆ [pre-commit.ci] pre-commit autoupdate. PR [#5196](https://github.com/tiangolo/fastapi/pull/5196) by [@pre-commit-ci[bot]](https://github.com/apps/pre-commit-ci).
* 🔥 Delete duplicated tests in `tests/test_tutorial/test_sql_databases/test_sql_databases.py`. PR [#5040](https://github.com/tiangolo/fastapi/pull/5040) by [@raccoonyy](https://github.com/raccoonyy).
* ♻ Simplify internal RegEx in `fastapi/utils.py`. PR [#5057](https://github.com/tiangolo/fastapi/pull/5057) by [@pylounge](https://github.com/pylounge).
* 🔧 Fix Type hint of `auto_error` which does not need to be `Optional[bool]`. PR [#4933](https://github.com/tiangolo/fastapi/pull/4933) by [@DavidKimDY](https://github.com/DavidKimDY).
* 🔧 Update mypy config, use `strict = true` instead of manual configs. PR [#4605](https://github.com/tiangolo/fastapi/pull/4605) by [@michaeloliverx](https://github.com/michaeloliverx).
* ♻ Change a `dict()` for `{}` in `fastapi/utils.py`. PR [#3138](https://github.com/tiangolo/fastapi/pull/3138) by [@ShahriyarR](https://github.com/ShahriyarR).
* ♻ Move internal variable for errors in `jsonable_encoder` to put related code closer. PR [#4560](https://github.com/tiangolo/fastapi/pull/4560) by [@GuilleQP](https://github.com/GuilleQP).
* ♻ Simplify conditional assignment in `fastapi/dependencies/utils.py`. PR [#4597](https://github.com/tiangolo/fastapi/pull/4597) by [@cikay](https://github.com/cikay).
* ⬆ Upgrade version pin accepted for Flake8, for internal code, to `flake8 >=3.8.3,=2.11.2,=1.1.0,= 3.7. PR [#1880](https://github.com/tiangolo/fastapi/pull/1880) by [@FFY00](https://github.com/FFY00).
* ⬆ Upgrade required Python version to >= 3.6.1, needed by typing.Deque, used by Pydantic. PR [#2733](https://github.com/tiangolo/fastapi/pull/2733) by [@hukkin](https://github.com/hukkin).
* ⬆️ Bump Uvicorn max range to 0.15.0. PR [#3345](https://github.com/tiangolo/fastapi/pull/3345) by [@Kludex](https://github.com/Kludex).

### Docs

* 📝 Update GraphQL docs, recommend Strawberry. PR [#3981](https://github.com/tiangolo/fastapi/pull/3981) by [@tiangolo](https://github.com/tiangolo).
* 📝 Re-write and extend Deployment guide: Concepts, Uvicorn, Gunicorn, Docker, Containers, Kubernetes. PR [#3974](https://github.com/tiangolo/fastapi/pull/3974) by [@tiangolo](https://github.com/tiangolo).
* 📝 Upgrade HTTPS guide with more explanations and diagrams. PR [#3950](https://github.com/tiangolo/fastapi/pull/3950) by [@tiangolo](https://github.com/tiangolo).

### Translations

* 🌐 Add Turkish translation for `docs/features.md`. PR [#1950](https://github.com/tiangolo/fastapi/pull/1950) by [@ycd](https://github.com/ycd).
* 🌐 Add Turkish translation for `docs/benchmarks.md`. PR [#2729](https://github.com/tiangolo/fastapi/pull/2729) by [@Telomeraz](https://github.com/Telomeraz).
* 🌐 Add Turkish translation for `docs/index.md`. PR [#1908](https://github.com/tiangolo/fastapi/pull/1908) by [@ycd](https://github.com/ycd).
* 🌐 Add French translation for `docs/tutorial/body.md`. PR [#3671](https://github.com/tiangolo/fastapi/pull/3671) by [@Smlep](https://github.com/Smlep).
* 🌐 Add French translation for `deployment/docker.md`. PR [#3694](https://github.com/tiangolo/fastapi/pull/3694) by [@rjNemo](https://github.com/rjNemo).
* 🌐 Add Portuguese translation for `docs/tutorial/path-params.md`. PR [#3664](https://github.com/tiangolo/fastapi/pull/3664) by [@FelipeSilva93](https://github.com/FelipeSilva93).
* 🌐 Add Portuguese translation for `docs/deployment/https.md`. PR [#3754](https://github.com/tiangolo/fastapi/pull/3754) by [@lsglucas](https://github.com/lsglucas).
* 🌐 Add German translation for `docs/features.md`. PR [#3699](https://github.com/tiangolo/fastapi/pull/3699) by [@mawassk](https://github.com/mawassk).

### Internal

* ✨ Update GitHub Action: notify-translations, to avoid a race conditions. PR [#3989](https://github.com/tiangolo/fastapi/pull/3989) by [@tiangolo](https://github.com/tiangolo).
* ⬆️ Upgrade development `autoflake`, supporting multi-line imports. PR [#3988](https://github.com/tiangolo/fastapi/pull/3988) by [@tiangolo](https://github.com/tiangolo).
* ⬆️ Increase dependency ranges for tests and docs: pytest-cov, pytest-asyncio, black, httpx, sqlalchemy, databases, mkdocs-markdownextradata-plugin. PR [#3987](https://github.com/tiangolo/fastapi/pull/3987) by [@tiangolo](https://github.com/tiangolo).
* 👥 Update FastAPI People. PR [#3986](https://github.com/tiangolo/fastapi/pull/3986) by [@github-actions[bot]](https://github.com/apps/github-actions).
* 💚 Fix badges in README and main page. PR [#3979](https://github.com/tiangolo/fastapi/pull/3979) by [@ghandic](https://github.com/ghandic).
* ⬆ Upgrade internal testing dependencies: mypy to version 0.910, add newly needed type packages. PR [#3350](https://github.com/tiangolo/fastapi/pull/3350) by [@ArcLightSlavik](https://github.com/ArcLightSlavik).
* ✨ Add Deepset Sponsorship. PR [#3976](https://github.com/tiangolo/fastapi/pull/3976) by [@tiangolo](https://github.com/tiangolo).
* 🎨 Tweak CSS styles for shell animations. PR [#3888](https://github.com/tiangolo/fastapi/pull/3888) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Add new Sponsor Calmcode.io. PR [#3777](https://github.com/tiangolo/fastapi/pull/3777) by [@tiangolo](https://github.com/tiangolo).

## 0.68.1 (2021-08-24)

* ✨ Add support for `read_with_orm_mode`, to support [SQLModel](https://sqlmodel.tiangolo.com/) relationship attributes. PR [#3757](https://github.com/tiangolo/fastapi/pull/3757) by [@tiangolo](https://github.com/tiangolo).

### Translations

* 🌐 Add Portuguese translation of `docs/fastapi-people.md`. PR [#3461](https://github.com/tiangolo/fastapi/pull/3461) by [@ComicShrimp](https://github.com/ComicShrimp).
* 🌐 Add Chinese translation for `docs/tutorial/dependencies/dependencies-in-path-operation-decorators.md`. PR [#3492](https://github.com/tiangolo/fastapi/pull/3492) by [@jaystone776](https://github.com/jaystone776).
* 🔧 Add new Translation tracking issues for German and Indonesian. PR [#3718](https://github.com/tiangolo/fastapi/pull/3718) by [@tiangolo](https://github.com/tiangolo).
* 🌐 Add Chinese translation for `docs/tutorial/dependencies/sub-dependencies.md`. PR [#3491](https://github.com/tiangolo/fastapi/pull/3491) by [@jaystone776](https://github.com/jaystone776).
* 🌐 Add Portuguese translation for `docs/advanced/index.md`. PR [#3460](https://github.com/tiangolo/fastapi/pull/3460) by [@ComicShrimp](https://github.com/ComicShrimp).
* 🌐 Portuguese translation of `docs/async.md`. PR [#1330](https://github.com/tiangolo/fastapi/pull/1330) by [@Serrones](https://github.com/Serrones).
* 🌐 Add French translation for `docs/async.md`. PR [#3416](https://github.com/tiangolo/fastapi/pull/3416) by [@Smlep](https://github.com/Smlep).

### Internal

* ✨ Add GitHub Action: Notify Translations. PR [#3715](https://github.com/tiangolo/fastapi/pull/3715) by [@tiangolo](https://github.com/tiangolo).
* ✨ Update computation of FastAPI People and sponsors. PR [#3714](https://github.com/tiangolo/fastapi/pull/3714) by [@tiangolo](https://github.com/tiangolo).
* ✨ Enable recent Material for MkDocs Insiders features. PR [#3710](https://github.com/tiangolo/fastapi/pull/3710) by [@tiangolo](https://github.com/tiangolo).
* 🔥 Remove/clean extra imports from examples in docs for features. PR [#3709](https://github.com/tiangolo/fastapi/pull/3709) by [@tiangolo](https://github.com/tiangolo).
* ➕ Update docs library to include sources in Markdown. PR [#3648](https://github.com/tiangolo/fastapi/pull/3648) by [@tiangolo](https://github.com/tiangolo).
* ⬆ Enable tests for Python 3.9. PR [#2298](https://github.com/tiangolo/fastapi/pull/2298) by [@Kludex](https://github.com/Kludex).
* 👥 Update FastAPI People. PR [#3642](https://github.com/tiangolo/fastapi/pull/3642) by [@github-actions[bot]](https://github.com/apps/github-actions).

## 0.68.0 (2021-07-29)

### Features

* ✨ Add support for extensions and updates to the OpenAPI schema in each *path operation*. New docs: [FastAPI Path Operation Advanced Configuration - OpenAPI Extra](https://fastapi.tiangolo.com/advanced/path-operation-advanced-configuration/#openapi-extra). Initial PR [#1922](https://github.com/tiangolo/fastapi/pull/1922) by [@edouardlp](https://github.com/edouardlp).
* ✨ Add additional OpenAPI metadata parameters to `FastAPI` class, shown on the automatic API docs UI. New docs: [Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/). Initial PR [#1812](https://github.com/tiangolo/fastapi/pull/1812) by [@dkreeft](https://github.com/dkreeft).
* ✨ Add `description` parameter to all the security scheme classes, e.g. `APIKeyQuery(name="key", description="A very cool API key")`. PR [#1757](https://github.com/tiangolo/fastapi/pull/1757) by [@hylkepostma](https://github.com/hylkepostma).
* ✨ Update OpenAPI models, supporting recursive models and extensions. PR [#3628](https://github.com/tiangolo/fastapi/pull/3628) by [@tiangolo](https://github.com/tiangolo).
* ✨ Import and re-export data structures from Starlette, used by Request properties, on `fastapi.datastructures`. Initial PR [#1872](https://github.com/tiangolo/fastapi/pull/1872) by [@jamescurtin](https://github.com/jamescurtin).

### Docs

* 📝 Update docs about async and response-model with more gender neutral language. PR [#1869](https://github.com/tiangolo/fastapi/pull/1869) by [@Edward-Knight](https://github.com/Edward-Knight).

### Translations

* 🌐 Add Russian translation for `docs/python-types.md`. PR [#3039](https://github.com/tiangolo/fastapi/pull/3039) by [@dukkee](https://github.com/dukkee).
* 🌐 Add Chinese translation for `docs/tutorial/dependencies/index.md`. PR [#3489](https://github.com/tiangolo/fastapi/pull/3489) by [@jaystone776](https://github.com/jaystone776).
* 🌐 Add Russian translation for `docs/external-links.md`. PR [#3036](https://github.com/tiangolo/fastapi/pull/3036) by [@dukkee](https://github.com/dukkee).
* 🌐 Add Chinese translation for `docs/tutorial/dependencies/global-dependencies.md`. PR [#3493](https://github.com/tiangolo/fastapi/pull/3493) by [@jaystone776](https://github.com/jaystone776).
* 🌐 Add Portuguese translation for `docs/deployment/versions.md`. PR [#3618](https://github.com/tiangolo/fastapi/pull/3618) by [@lsglucas](https://github.com/lsglucas).
* 🌐 Add Japanese translation for `docs/tutorial/security/oauth2-jwt.md`. PR [#3526](https://github.com/tiangolo/fastapi/pull/3526) by [@sattosan](https://github.com/sattosan).

### Internal

* ✅ Add  the `docs_src` directory to test coverage and update tests. Initial PR [#1904](https://github.com/tiangolo/fastapi/pull/1904) by [@Kludex](https://github.com/Kludex).
* 🔧 Add new GitHub templates with forms for new issues. PR [#3612](https://github.com/tiangolo/fastapi/pull/3612) by [@tiangolo](https://github.com/tiangolo).
* 📝 Add official FastAPI Twitter to docs: [@fastapi](https://x.com/fastapi). PR [#3578](https://github.com/tiangolo/fastapi/pull/3578) by [@tiangolo](https://github.com/tiangolo).

## 0.67.0 (2021-07-21)

### Features

* ✨ Add support for `dataclasses` in request bodies and `response_model`. New documentation: [Advanced User Guide - Using Dataclasses](https://fastapi.tiangolo.com/advanced/dataclasses/). PR [#3577](https://github.com/tiangolo/fastapi/pull/3577) by [@tiangolo](https://github.com/tiangolo).
* ✨ Support `dataclasses` in responses. PR [#3576](https://github.com/tiangolo/fastapi/pull/3576) by [@tiangolo](https://github.com/tiangolo), continuation from initial PR [#2722](https://github.com/tiangolo/fastapi/pull/2722) by [@amitlissack](https://github.com/amitlissack).

### Docs

* 📝 Add external link: How to Create A Fake Certificate Authority And Generate TLS Certs for FastAPI. PR [#2839](https://github.com/tiangolo/fastapi/pull/2839) by [@aitoehigie](https://github.com/aitoehigie).
* ✏ Fix code highlighted line in: `body-nested-models.md`. PR [#3463](https://github.com/tiangolo/fastapi/pull/3463) by [@jaystone776](https://github.com/jaystone776).
* ✏ Fix typo in `body-nested-models.md`. PR [#3462](https://github.com/tiangolo/fastapi/pull/3462) by [@jaystone776](https://github.com/jaystone776).
* ✏ Fix typo "might me" -> "might be" in `docs/en/docs/tutorial/schema-extra-example.md`. PR [#3362](https://github.com/tiangolo/fastapi/pull/3362) by [@dbrakman](https://github.com/dbrakman).
* 📝 Add external link: Building simple E-Commerce with NuxtJS and FastAPI. PR [#3271](https://github.com/tiangolo/fastapi/pull/3271) by [@ShahriyarR](https://github.com/ShahriyarR).
* 📝 Add external link: Serve a machine learning model using Sklearn, FastAPI and Docker. PR [#2974](https://github.com/tiangolo/fastapi/pull/2974) by [@rodrigo-arenas](https://github.com/rodrigo-arenas).
* ✏️ Fix typo on docstring in datastructures file. PR [#2887](https://github.com/tiangolo/fastapi/pull/2887) by [@Kludex](https://github.com/Kludex).
* 📝 Add External Link: Deploy FastAPI on Ubuntu and Serve using Caddy 2 Web Server. PR [#3572](https://github.com/tiangolo/fastapi/pull/3572) by [@tiangolo](https://github.com/tiangolo).
* 📝 Add External Link, replaces #1898. PR [#3571](https://github.com/tiangolo/fastapi/pull/3571) by [@tiangolo](https://github.com/tiangolo).

### Internal

* 🎨 Improve style for sponsors, add radius border. PR [#2388](https://github.com/tiangolo/fastapi/pull/2388) by [@Kludex](https://github.com/Kludex).
* 👷 Update GitHub Action latest-changes. PR [#3574](https://github.com/tiangolo/fastapi/pull/3574) by [@tiangolo](https://github.com/tiangolo).
* 👷 Update GitHub Action latest-changes. PR [#3573](https://github.com/tiangolo/fastapi/pull/3573) by [@tiangolo](https://github.com/tiangolo).
* 👷 Rename and clarify CI workflow job names. PR [#3570](https://github.com/tiangolo/fastapi/pull/3570) by [@tiangolo](https://github.com/tiangolo).
* 👷 Update GitHub Action latest-changes, strike 2 ⚾. PR [#3575](https://github.com/tiangolo/fastapi/pull/3575) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Sort external links in docs to have the most recent at the top. PR [#3568](https://github.com/tiangolo/fastapi/pull/3568) by [@tiangolo](https://github.com/tiangolo).

## 0.66.1 (2021-07-19)

### Translations

* 🌐 Add basic setup for German translations. PR [#3522](https://github.com/tiangolo/fastapi/pull/3522) by [@0x4Dark](https://github.com/0x4Dark).
* 🌐 Add Portuguese translation for `docs/tutorial/security/index.md`. PR [#3507](https://github.com/tiangolo/fastapi/pull/3507) by [@oandersonmagalhaes](https://github.com/oandersonmagalhaes).
* 🌐 Add Portuguese translation for `docs/deployment/index.md`. PR [#3337](https://github.com/tiangolo/fastapi/pull/3337) by [@lsglucas](https://github.com/lsglucas).

### Internal

* 🔧 Configure strict pytest options and update/refactor tests. Upgrade pytest to `>=6.2.4,=2.12.0,=3.3.0,=0.0.12 to fix conflicts. PR [#3429](https://github.com/tiangolo/fastapi/pull/3429) by [@tiangolo](https://github.com/tiangolo).

## 0.65.2 (2021-06-09)

### Security fixes

* 🔒 Check Content-Type request header before assuming JSON. Initial PR [#2118](https://github.com/tiangolo/fastapi/pull/2118) by [@patrickkwang](https://github.com/patrickkwang).

This change fixes a [CSRF](https://en.wikipedia.org/wiki/Cross-site_request_forgery) security vulnerability when using cookies for authentication in path operations with JSON payloads sent by browsers.

In versions lower than `0.65.2`, FastAPI would try to read the request payload as JSON even if the `content-type` header sent was not set to `application/json` or a compatible JSON media type (e.g. `application/geo+json`).

So, a request with a content type of `text/plain` containing JSON data would be accepted and the JSON data would be extracted.

But requests with content type `text/plain` are exempt from [CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS) preflights, for being considered [Simple requests](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS#simple_requests). So, the browser would execute them right away including cookies, and the text content could be a JSON string that would be parsed and accepted by the FastAPI application.

See [CVE-2021-32677](https://github.com/tiangolo/fastapi/security/advisories/GHSA-8h2j-cgx8-6xv7) for more details.

Thanks to [Dima Boger](https://x.com/b0g3r) for the security report! 🙇🔒

### Internal

* 🔧 Update sponsors badge, course bundle. PR [#3340](https://github.com/tiangolo/fastapi/pull/3340) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Add new gold sponsor Jina 🎉. PR [#3291](https://github.com/tiangolo/fastapi/pull/3291) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Add new banner sponsor badge for FastAPI courses bundle. PR [#3288](https://github.com/tiangolo/fastapi/pull/3288) by [@tiangolo](https://github.com/tiangolo).
* 👷 Upgrade Issue Manager GitHub Action. PR [#3236](https://github.com/tiangolo/fastapi/pull/3236) by [@tiangolo](https://github.com/tiangolo).

## 0.65.1 (2021-05-11)

### Security fixes

* 📌 Upgrade pydantic pin, to handle security vulnerability [CVE-2021-29510](https://github.com/pydantic/pydantic/security/advisories/GHSA-5jqp-qgf6-3pvh). PR [#3213](https://github.com/tiangolo/fastapi/pull/3213) by [@tiangolo](https://github.com/tiangolo).

## 0.65.0 (2021-05-10)

### Breaking Changes - Upgrade

* ⬆️  Upgrade Starlette to `0.14.2`, including internal `UJSONResponse` migrated from Starlette. This includes several bug fixes and features from Starlette. PR [#2335](https://github.com/tiangolo/fastapi/pull/2335) by [@hanneskuettner](https://github.com/hanneskuettner).

### Translations

* 🌐 Initialize new language Polish for translations. PR [#3170](https://github.com/tiangolo/fastapi/pull/3170) by [@neternefer](https://github.com/neternefer).

### Internal

* 👷 Add GitHub Action cache to speed up CI installs. PR [#3204](https://github.com/tiangolo/fastapi/pull/3204) by [@tiangolo](https://github.com/tiangolo).
* ⬆️ Upgrade setup-python GitHub Action to v2. PR [#3203](https://github.com/tiangolo/fastapi/pull/3203) by [@tiangolo](https://github.com/tiangolo).
* 🐛 Fix docs script to generate a new translation language with `overrides` boilerplate. PR [#3202](https://github.com/tiangolo/fastapi/pull/3202) by [@tiangolo](https://github.com/tiangolo).
* ✨ Add new Deta banner badge with new sponsorship tier 🙇. PR [#3194](https://github.com/tiangolo/fastapi/pull/3194) by [@tiangolo](https://github.com/tiangolo).
* 👥 Update FastAPI People. PR [#3189](https://github.com/tiangolo/fastapi/pull/3189) by [@github-actions[bot]](https://github.com/apps/github-actions).
* 🔊 Update FastAPI People to allow better debugging. PR [#3188](https://github.com/tiangolo/fastapi/pull/3188) by [@tiangolo](https://github.com/tiangolo).

## 0.64.0 (2021-05-07)

### Features

* ✨ Add support for adding multiple `examples` in request bodies and path, query, cookie, and header params. New docs: [Declare Request Example Data](https://fastapi.tiangolo.com/tutorial/schema-extra-example/#body-with-multiple-examples). Initial PR [#1267](https://github.com/tiangolo/fastapi/pull/1267) by [@austinorr](https://github.com/austinorr).

### Fixes

* 📌 Pin SQLAlchemy range for tests, as it doesn't use SemVer. PR [#3001](https://github.com/tiangolo/fastapi/pull/3001) by [@tiangolo](https://github.com/tiangolo).
* 🎨 Add newly required type annotations for mypy. PR [#2882](https://github.com/tiangolo/fastapi/pull/2882) by [@tiangolo](https://github.com/tiangolo).
* 🎨 Remove internal "type: ignore", now unnecessary. PR [#2424](https://github.com/tiangolo/fastapi/pull/2424) by [@AsakuraMizu](https://github.com/AsakuraMizu).

### Docs

* 📝 Add link to article in Russian "FastAPI: знакомимся с фреймворком". PR [#2564](https://github.com/tiangolo/fastapi/pull/2564) by [@trkohler](https://github.com/trkohler).
* 📝 Add external link to blog post "Authenticate Your FastAPI App with Auth0". PR [#2172](https://github.com/tiangolo/fastapi/pull/2172) by [@dompatmore](https://github.com/dompatmore).
* 📝 Fix broken link to article: Machine learning model serving in Python using FastAPI and Streamlit. PR [#2557](https://github.com/tiangolo/fastapi/pull/2557) by [@davidefiocco](https://github.com/davidefiocco).
* 📝 Add FastAPI Medium Article: Deploy a dockerized FastAPI application to AWS. PR [#2515](https://github.com/tiangolo/fastapi/pull/2515) by [@vjanz](https://github.com/vjanz).
* ✏ Fix typo in Tutorial - Handling Errors. PR [#2486](https://github.com/tiangolo/fastapi/pull/2486) by [@johnthagen](https://github.com/johnthagen).
* ✏ Fix typo in Security OAuth2 scopes. PR [#2407](https://github.com/tiangolo/fastapi/pull/2407) by [@jugmac00](https://github.com/jugmac00).
* ✏ Fix typo/clarify docs for SQL (Relational) Databases. PR [#2393](https://github.com/tiangolo/fastapi/pull/2393) by [@kangni](https://github.com/kangni).
* 📝 Add external link to "FastAPI for Flask Users". PR [#2280](https://github.com/tiangolo/fastapi/pull/2280) by [@amitness](https://github.com/amitness).

### Translations

* 🌐 Fix Chinese translation of Tutorial - Query Parameters, remove obsolete content. PR [#3051](https://github.com/tiangolo/fastapi/pull/3051) by [@louis70109](https://github.com/louis70109).
* 🌐 Add French translation for Tutorial - Background Tasks. PR [#3098](https://github.com/tiangolo/fastapi/pull/3098) by [@Smlep](https://github.com/Smlep).
* 🌐 Fix Korean translation for docs/ko/docs/index.md. PR [#3159](https://github.com/tiangolo/fastapi/pull/3159) by [@SueNaEunYang](https://github.com/SueNaEunYang).
* 🌐 Add Korean translation for Tutorial - Query Parameters. PR [#2390](https://github.com/tiangolo/fastapi/pull/2390) by [@hard-coders](https://github.com/hard-coders).
* 🌐 Add French translation for FastAPI People. PR [#2232](https://github.com/tiangolo/fastapi/pull/2232) by [@JulianMaurin](https://github.com/JulianMaurin).
* 🌐 Add Korean translation for Tutorial - Path Parameters. PR [#2355](https://github.com/tiangolo/fastapi/pull/2355) by [@hard-coders](https://github.com/hard-coders).
* 🌐 Add French translation for Features. PR [#2157](https://github.com/tiangolo/fastapi/pull/2157) by [@Jefidev](https://github.com/Jefidev).
* 👥 Update FastAPI People. PR [#3031](https://github.com/tiangolo/fastapi/pull/3031) by [@github-actions[bot]](https://github.com/apps/github-actions).
* 🌐 Add Chinese translation for Tutorial - Debugging. PR [#2737](https://github.com/tiangolo/fastapi/pull/2737) by [@blt232018](https://github.com/blt232018).
* 🌐 Add Chinese translation for Tutorial - Security - OAuth2 with Password (and hashing), Bearer with JWT tokens. PR [#2642](https://github.com/tiangolo/fastapi/pull/2642) by [@waynerv](https://github.com/waynerv).
* 🌐 Add Korean translation for Tutorial - Header Parameters. PR [#2589](https://github.com/tiangolo/fastapi/pull/2589) by [@mode9](https://github.com/mode9).
* 🌐 Add Chinese translation for Tutorial - Metadata and Docs URLs. PR [#2559](https://github.com/tiangolo/fastapi/pull/2559) by [@blt232018](https://github.com/blt232018).
* 🌐 Add Korean translation for Tutorial - First Steps. PR [#2323](https://github.com/tiangolo/fastapi/pull/2323) by [@hard-coders](https://github.com/hard-coders).
* 🌐 Add Chinese translation for Tutorial - CORS (Cross-Origin Resource Sharing). PR [#2540](https://github.com/tiangolo/fastapi/pull/2540) by [@blt232018](https://github.com/blt232018).
* 🌐 Add Chinese translation for Tutorial - Middleware. PR [#2334](https://github.com/tiangolo/fastapi/pull/2334) by [@lpdswing](https://github.com/lpdswing).
* 🌐 Add Korean translation for Tutorial - Intro. PR [#2317](https://github.com/tiangolo/fastapi/pull/2317) by [@hard-coders](https://github.com/hard-coders).
* 🌐 Add Chinese translation for Tutorial - Bigger Applications - Multiple Files. PR [#2453](https://github.com/tiangolo/fastapi/pull/2453) by [@waynerv](https://github.com/waynerv).
* 🌐 Add Chinese translation for Tutorial - Security - Security Intro. PR [#2443](https://github.com/tiangolo/fastapi/pull/2443) by [@waynerv](https://github.com/waynerv).
* 🌐 Add Chinese translation for Tutorial - Header Parameters. PR [#2412](https://github.com/tiangolo/fastapi/pull/2412) by [@maoyibo](https://github.com/maoyibo).
* 🌐 Add Chinese translation for Tutorial - Extra Data Types. PR [#2410](https://github.com/tiangolo/fastapi/pull/2410) by [@maoyibo](https://github.com/maoyibo).
* 🌐 Add Japanese translation for Deployment - Docker. PR [#2312](https://github.com/tiangolo/fastapi/pull/2312) by [@tokusumi](https://github.com/tokusumi).
* 🌐 Add Japanese translation for Deployment - Versions. PR [#2310](https://github.com/tiangolo/fastapi/pull/2310) by [@tokusumi](https://github.com/tokusumi).
* 🌐 Add Chinese translation for Tutorial - Cookie Parameters. PR [#2261](https://github.com/tiangolo/fastapi/pull/2261) by [@alicrazy1947](https://github.com/alicrazy1947).
* 🌐 Add Japanese translation for Tutorial - Static files. PR [#2260](https://github.com/tiangolo/fastapi/pull/2260) by [@tokusumi](https://github.com/tokusumi).
* 🌐 Add Japanese translation for Tutorial - Testing. PR [#2259](https://github.com/tiangolo/fastapi/pull/2259) by [@tokusumi](https://github.com/tokusumi).
* 🌐 Add Japanese translation for Tutorial - Debugging. PR [#2256](https://github.com/tiangolo/fastapi/pull/2256) by [@tokusumi](https://github.com/tokusumi).
* 🌐 Add Japanese translation for Tutorial - Middleware. PR [#2255](https://github.com/tiangolo/fastapi/pull/2255) by [@tokusumi](https://github.com/tokusumi).
* 🌐 Add Japanese translation for Concurrency and async / await. PR [#2058](https://github.com/tiangolo/fastapi/pull/2058) by [@tokusumi](https://github.com/tokusumi).
* 🌐 Add Chinese translation for Tutorial - Security - Simple OAuth2 with Password and Bearer. PR [#2514](https://github.com/tiangolo/fastapi/pull/2514) by [@waynerv](https://github.com/waynerv).
* 🌐 Add Japanese translation for Deployment - Deta. PR [#2314](https://github.com/tiangolo/fastapi/pull/2314) by [@tokusumi](https://github.com/tokusumi).
* 🌐 Add Chinese translation for Tutorial - Security - Get Current User. PR [#2474](https://github.com/tiangolo/fastapi/pull/2474) by [@waynerv](https://github.com/waynerv).
* 🌐 Add Japanese translation for Deployment - Manually. PR [#2313](https://github.com/tiangolo/fastapi/pull/2313) by [@tokusumi](https://github.com/tokusumi).
* 🌐 Add Japanese translation for Deployment - Intro. PR [#2309](https://github.com/tiangolo/fastapi/pull/2309) by [@tokusumi](https://github.com/tokusumi).
* 🌐 Add Japanese translation for FastAPI People. PR [#2254](https://github.com/tiangolo/fastapi/pull/2254) by [@tokusumi](https://github.com/tokusumi).
* 🌐 Add Japanese translation for Advanced - Path Operation Advanced Configuration. PR [#2124](https://github.com/tiangolo/fastapi/pull/2124) by [@Attsun1031](https://github.com/Attsun1031).
* 🌐 Add Japanese translation for External Links. PR [#2070](https://github.com/tiangolo/fastapi/pull/2070) by [@tokusumi](https://github.com/tokusumi).
* 🌐 Add Japanese translation for Tutorial - Body - Updates. PR [#1956](https://github.com/tiangolo/fastapi/pull/1956) by [@SwftAlpc](https://github.com/SwftAlpc).
* 🌐 Add Japanese translation for Tutorial - Form Data. PR [#1943](https://github.com/tiangolo/fastapi/pull/1943) by [@SwftAlpc](https://github.com/SwftAlpc).
* 🌐 Add Japanese translation for Tutorial - Cookie Parameters. PR [#1933](https://github.com/tiangolo/fastapi/pull/1933) by [@SwftAlpc](https://github.com/SwftAlpc).

### Internal

* 🔧 Update top banner, point to newsletter. PR [#3003](https://github.com/tiangolo/fastapi/pull/3003) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Disable sponsor WeTransfer. PR [#3002](https://github.com/tiangolo/fastapi/pull/3002) by [@tiangolo](https://github.com/tiangolo).
* 👥 Update FastAPI People. PR [#2880](https://github.com/tiangolo/fastapi/pull/2880) by [@github-actions[bot]](https://github.com/apps/github-actions).
* 👥 Update FastAPI People. PR [#2739](https://github.com/tiangolo/fastapi/pull/2739) by [@github-actions[bot]](https://github.com/apps/github-actions).
* 🔧 Add new Gold Sponsor Talk Python 🎉. PR [#2673](https://github.com/tiangolo/fastapi/pull/2673) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Add new Gold Sponsor vim.so 🎉. PR [#2669](https://github.com/tiangolo/fastapi/pull/2669) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Add FastAPI user survey banner. PR [#2623](https://github.com/tiangolo/fastapi/pull/2623) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Add new Bronze Sponsor(s) 🥉🎉. PR [#2622](https://github.com/tiangolo/fastapi/pull/2622) by [@tiangolo](https://github.com/tiangolo).
* 📝 Update social links: add Discord, fix GitHub. PR [#2621](https://github.com/tiangolo/fastapi/pull/2621) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Update FastAPI People GitHub Sponsors order. PR [#2620](https://github.com/tiangolo/fastapi/pull/2620) by [@tiangolo](https://github.com/tiangolo).
* 🔧 Update InvestSuite sponsor data. PR [#2608](https://github.com/tiangolo/fastapi/pull/2608) by [@tiangolo](https://github.com/tiangolo).
* 👥 Update FastAPI People. PR [#2590](https://github.com/tiangolo/fastapi/pull/2590) by [@github-actions[bot]](https://github.com/apps/github-actions).

## 0.63.0 (2020-12-20)

### Features

* ✨ Improve type annotations, add support for mypy --strict, internally and for external packages. PR [#2547](https://github.com/tiangolo/fastapi/pull/2547) by [@tiangolo](https://github.com/tiangolo).

### Breaking changes

* ⬆️ Upgrade Uvicorn when installing `fastapi[all]` to the latest version including `uvloop`, the new range is `uvicorn[standard] >=0.12.0, `1.0.0`.
    * Remove support for deprecated Pydantic `0.32.2`. This improves maintainability and allows new features.
    * In `FastAPI` and `APIRouter`:
        * Remove *path operation decorators* related/deprecated parameter `response_model_skip_defaults` (use `response_model_exclude_unset` instead).
        * Change *path operation decorators* parameter default for `response_model_exclude` from `set()` to `None` (as is in Pydantic).
    * In `encoders.jsonable_encoder`:
        * Remove deprecated `skip_defaults`, use instead `exclude_unset`.
        * Set default of `exclude` from `set()` to `None` (as is in Pydantic).
    * PR [#1862](https://github.com/tiangolo/fastapi/pull/1862).
* In `encoders.jsonable_encoder` remove parameter `sqlalchemy_safe`.
    * It was an early hack to allow returning SQLAlchemy models, but it was never documented, and the recommended way is using Pydantic's `orm_mode` as described in the tutorial: [SQL (Relational) Databases](https://fastapi.tiangolo.com/tutorial/sql-databases/).
    * PR [#1864](https://github.com/tiangolo/fastapi/pull/1864).

### Docs

* Add link to the course by TestDriven.io: [Test-Driven Development with FastAPI and Docker](https://testdriven.io/courses/tdd-fastapi/). PR [#1860](https://github.com/tiangolo/fastapi/pull/1860).
* Fix empty log message in docs example about handling errors. PR [#1815](https://github.com/tiangolo/fastapi/pull/1815) by [@manlix](https://github.com/manlix).
* Reword text to reduce ambiguity while not being gender-specific. PR [#1824](https://github.com/tiangolo/fastapi/pull/1824) by [@Mause](https://github.com/Mause).

### Internal

* Add Flake8 linting. Original PR [#1774](https://github.com/tiangolo/fastapi/pull/1774) by [@MashhadiNima](https://github.com/MashhadiNima).
* Disable Gitter bot, as it's currently broken, and Gitter's response doesn't show the problem. PR [#1853](https://github.com/tiangolo/fastapi/pull/1853).

## 0.60.2 (2020-08-08)

* Fix typo in docs for query parameters. PR [#1832](https://github.com/tiangolo/fastapi/pull/1832) by [@ycd](https://github.com/ycd).
* Add docs about [Async Tests](https://fastapi.tiangolo.com/advanced/async-tests/). PR [#1619](https://github.com/tiangolo/fastapi/pull/1619) by [@empicano](https://github.com/empicano).
* Raise an exception when using form data (`Form`, `File`) without having `python-multipart` installed.
    * Up to now the application would run, and raise an exception only when receiving a request with form data, the new behavior, raising early, will prevent from deploying applications with broken dependencies.
    * It also detects if the correct package `python-multipart` is installed instead of the incorrect `multipart` (both importable as `multipart`).
    * PR [#1851](https://github.com/tiangolo/fastapi/pull/1851) based on original PR [#1627](https://github.com/tiangolo/fastapi/pull/1627) by [@chrisngyn](https://github.com/chrisngyn), [@YKo20010](https://github.com/YKo20010), [@kx-chen](https://github.com/kx-chen).
* Re-enable Gitter releases bot. PR [#1831](https://github.com/tiangolo/fastapi/pull/1831).
* Add link to async SQL databases tutorial from main SQL tutorial. PR [#1813](https://github.com/tiangolo/fastapi/pull/1813) by [@short2strings](https://github.com/short2strings).
* Fix typo in tutorial about behind a proxy. PR [#1807](https://github.com/tiangolo/fastapi/pull/1807) by [@toidi](https://github.com/toidi).
* Fix typo in Portuguese docs. PR [#1795](https://github.com/tiangolo/fastapi/pull/1795) by [@izaguerreiro](https://github.com/izaguerreiro).
* Add translations setup for Ukrainian. PR [#1830](https://github.com/tiangolo/fastapi/pull/1830).
* Add external link [Build And Host Fast Data Science Applications Using FastAPI](https://towardsdatascience.com/build-and-host-fast-data-science-applications-using-fastapi-823be8a1d6a0). PR [#1786](https://github.com/tiangolo/fastapi/pull/1786) by [@Kludex](https://github.com/Kludex).
* Fix encoding of Pydantic models that inherit from others models with custom `json_encoders`. PR [#1769](https://github.com/tiangolo/fastapi/pull/1769) by [@henrybetts](https://github.com/henrybetts).
* Simplify and improve `jsonable_encoder`. PR [#1754](https://github.com/tiangolo/fastapi/pull/1754) by [@MashhadiNima](https://github.com/MashhadiNima).
* Simplify internal code syntax in several points. PR [#1753](https://github.com/tiangolo/fastapi/pull/1753) by [@uriyyo](https://github.com/uriyyo).
* Improve internal typing, declare `Optional` parameters. PR [#1731](https://github.com/tiangolo/fastapi/pull/1731) by [@MashhadiNima](https://github.com/MashhadiNima).
* Add external link [Deploy FastAPI on Azure App Service](https://www.tutlinks.com/deploy-fastapi-on-azure/) to docs. PR [#1726](https://github.com/tiangolo/fastapi/pull/1726) by [@windson](https://github.com/windson).
* Add link to Starlette docs about WebSocket testing. PR [#1717](https://github.com/tiangolo/fastapi/pull/1717) by [@hellocoldworld](https://github.com/hellocoldworld).
* Refactor generating dependant, merge for loops. PR [#1714](https://github.com/tiangolo/fastapi/pull/1714) by [@Bloodielie](https://github.com/Bloodielie).
* Update example for templates with Jinja to include HTML media type. PR [#1690](https://github.com/tiangolo/fastapi/pull/1690) by [@frafra](https://github.com/frafra).
* Fix typos in docs for security. PR [#1678](https://github.com/tiangolo/fastapi/pull/1678) by [@nilslindemann](https://github.com/nilslindemann).
* Fix typos in docs for dependencies. PR [#1675](https://github.com/tiangolo/fastapi/pull/1675) by [@nilslindemann](https://github.com/nilslindemann).
* Fix type annotation for `**extra` parameters in `FastAPI`. PR [#1659](https://github.com/tiangolo/fastapi/pull/1659) by [@bharel](https://github.com/bharel).
* Bump MkDocs Material to fix docs in browsers with dark mode. PR [#1789](https://github.com/tiangolo/fastapi/pull/1789) by [@adriencaccia](https://github.com/adriencaccia).
* Remove docs preview comment from each commit. PR [#1826](https://github.com/tiangolo/fastapi/pull/1826).
* Update GitHub context extraction for Gitter notification bot. PR [#1766](https://github.com/tiangolo/fastapi/pull/1766).

## 0.60.1 (2020-07-22)

* Add debugging logs for GitHub actions to introspect GitHub hidden context. PR [#1764](https://github.com/tiangolo/fastapi/pull/1764).
* Use OS preference theme for online docs. PR [#1760](https://github.com/tiangolo/fastapi/pull/1760) by [@adriencaccia](https://github.com/adriencaccia).
* Upgrade Starlette to version `0.13.6` to handle a vulnerability when using static files in Windows. PR [#1759](https://github.com/tiangolo/fastapi/pull/1759) by [@jamesag26](https://github.com/jamesag26).
* Pin Swagger UI temporarily, waiting for a fix for [swagger-api/swagger-ui#6249](https://github.com/swagger-api/swagger-ui/issues/6249). PR [#1763](https://github.com/tiangolo/fastapi/pull/1763).
* Update GitHub Actions, use commit from PR for docs preview, not commit from pre-merge. PR [#1761](https://github.com/tiangolo/fastapi/pull/1761).
* Update GitHub Actions, refactor Gitter bot. PR [#1746](https://github.com/tiangolo/fastapi/pull/1746).

## 0.60.0 (2020-07-20)

* Add GitHub Action to watch for missing preview docs and trigger a preview deploy. PR [#1740](https://github.com/tiangolo/fastapi/pull/1740).
* Add custom GitHub Action to get artifact with docs preview. PR [#1739](https://github.com/tiangolo/fastapi/pull/1739).
* Add new GitHub Actions to preview docs from PRs. PR [#1738](https://github.com/tiangolo/fastapi/pull/1738).
* Add XML test coverage to support GitHub Actions. PR [#1737](https://github.com/tiangolo/fastapi/pull/1737).
* Update badges and remove Travis now that GitHub Actions is the main CI. PR [#1736](https://github.com/tiangolo/fastapi/pull/1736).
* Add GitHub Actions for CI, move from Travis. PR [#1735](https://github.com/tiangolo/fastapi/pull/1735).
* Add support for adding OpenAPI schema for GET requests with a body. PR [#1626](https://github.com/tiangolo/fastapi/pull/1626) by [@victorphoenix3](https://github.com/victorphoenix3).

## 0.59.0 (2020-07-10)

* Fix typo in docstring for OAuth2 utils. PR [#1621](https://github.com/tiangolo/fastapi/pull/1621) by [@tomarv2](https://github.com/tomarv2).
* Update JWT docs to use Python-jose instead of PyJWT. Initial PR [#1610](https://github.com/tiangolo/fastapi/pull/1610) by [@asheux](https://github.com/asheux).
* Fix/re-enable search bar in docs. PR [#1703](https://github.com/tiangolo/fastapi/pull/1703).
* Auto-generate a "server" in OpenAPI `servers` when there's a `root_path` instead of prefixing all the `paths`:
    * Add a new parameter for `FastAPI` classes: `root_path_in_servers` to disable the auto-generation of `servers`.
    * New docs about `root_path` and `servers` in [Additional Servers](https://fastapi.tiangolo.com/advanced/behind-a-proxy/#additional-servers).
    * Update OAuth2 examples to use a relative URL for `tokenUrl="token"` to make sure those examples keep working as-is even when behind a reverse proxy.
    * Initial PR [#1596](https://github.com/tiangolo/fastapi/pull/1596) by [@rkbeatss](https://github.com/rkbeatss).
* Fix typo/link in External Links. PR [#1702](https://github.com/tiangolo/fastapi/pull/1702).
* Update handling of [External Links](https://fastapi.tiangolo.com/external-links/) to use a data file and allow translating the headers without becoming obsolete quickly when new links are added. PR [#https://github.com/tiangolo/fastapi/pull/1701](https://github.com/tiangolo/fastapi/pull/1701).
* Add external link [Machine learning model serving in Python using FastAPI and Streamlit](https://davidefiocco.github.io/2020/06/27/streamlit-fastapi-ml-serving.html) to docs. PR [#1669](https://github.com/tiangolo/fastapi/pull/1669) by [@davidefiocco](https://github.com/davidefiocco).
* Add note in docs on order in Pydantic Unions. PR [#1591](https://github.com/tiangolo/fastapi/pull/1591) by [@kbanc](https://github.com/kbanc).
* Improve support for tests in editor. PR [#1699](https://github.com/tiangolo/fastapi/pull/1699).
* Pin dependencies. PR [#1697](https://github.com/tiangolo/fastapi/pull/1697).
* Update isort to version 5.x.x. PR [#1670](https://github.com/tiangolo/fastapi/pull/1670) by [@asheux](https://github.com/asheux).

## 0.58.1 (2020-06-28)

* Add link in docs to Pydantic data types. PR [#1612](https://github.com/tiangolo/fastapi/pull/1612) by [@tayoogunbiyi](https://github.com/tayoogunbiyi).
* Fix link in warning logs for `openapi_prefix`. PR [#1611](https://github.com/tiangolo/fastapi/pull/1611) by [@bavaria95](https://github.com/bavaria95).
* Fix bad link in docs. PR [#1603](https://github.com/tiangolo/fastapi/pull/1603) by [@molto0504](https://github.com/molto0504).
* Add Vim temporary files to `.gitignore` for contributors using Vim. PR [#1590](https://github.com/tiangolo/fastapi/pull/1590) by [@asheux](https://github.com/asheux).
* Fix typo in docs for sub-applications. PR [#1578](https://github.com/tiangolo/fastapi/pull/1578) by [@schlpbch](https://github.com/schlpbch).
* Use `Optional` in all the examples in the docs. Original PR [#1574](https://github.com/tiangolo/fastapi/pull/1574) by [@chrisngyn](https://github.com/chrisngyn), [@kx-chen](https://github.com/kx-chen), [@YKo20010](https://github.com/YKo20010). Updated and merged PR [#1644](https://github.com/tiangolo/fastapi/pull/1644).
* Update tests and handling of `response_model_by_alias`. PR [#1642](https://github.com/tiangolo/fastapi/pull/1642).
* Add translation to Chinese for [Body - Fields - 请求体 - 字段](https://fastapi.tiangolo.com/zh/tutorial/body-fields/). PR [#1569](https://github.com/tiangolo/fastapi/pull/1569) by [@waynerv](https://github.com/waynerv).
* Update Chinese translation of main page. PR [#1564](https://github.com/tiangolo/fastapi/pull/1564) by [@waynerv](https://github.com/waynerv).
* Add translation to Chinese for [Body - Multiple Parameters - 请求体 - 多个参数](https://fastapi.tiangolo.com/zh/tutorial/body-multiple-params/). PR [#1532](https://github.com/tiangolo/fastapi/pull/1532) by [@waynerv](https://github.com/waynerv).
* Add translation to Chinese for [Path Parameters and Numeric Validations - 路径参数和数值校验](https://fastapi.tiangolo.com/zh/tutorial/path-params-numeric-validations/). PR [#1506](https://github.com/tiangolo/fastapi/pull/1506) by [@waynerv](https://github.com/waynerv).
* Add GitHub action to auto-label approved PRs (mainly for translations). PR [#1638](https://github.com/tiangolo/fastapi/pull/1638).

## 0.58.0 (2020-06-15)

* Deep merge OpenAPI responses to preserve all the additional metadata. PR [#1577](https://github.com/tiangolo/fastapi/pull/1577).
* Mention in docs that only main app events are run (not sub-apps). PR [#1554](https://github.com/tiangolo/fastapi/pull/1554) by [@amacfie](https://github.com/amacfie).
* Fix body validation error response, do not include body variable when it is not embedded. PR [#1553](https://github.com/tiangolo/fastapi/pull/1553) by [@amacfie](https://github.com/amacfie).
* Fix testing OAuth2 security scopes when using dependency overrides. PR [#1549](https://github.com/tiangolo/fastapi/pull/1549) by [@amacfie](https://github.com/amacfie).
* Fix Model for JSON Schema keyword `not` as a JSON Schema instead of a list. PR [#1548](https://github.com/tiangolo/fastapi/pull/1548) by [@v-do](https://github.com/v-do).
* Add support for OpenAPI `servers`. PR [#1547](https://github.com/tiangolo/fastapi/pull/1547) by [@mikaello](https://github.com/mikaello).

## 0.57.0 (2020-06-13)

* Remove broken link from "External Links". PR [#1565](https://github.com/tiangolo/fastapi/pull/1565) by [@victorphoenix3](https://github.com/victorphoenix3).
* Update/fix docs for [WebSockets with dependencies](https://fastapi.tiangolo.com/advanced/websockets/#using-depends-and-others). Original PR [#1540](https://github.com/tiangolo/fastapi/pull/1540) by [@ChihSeanHsu](https://github.com/ChihSeanHsu).
* Add support for Python's `http.HTTPStatus` in `status_code` parameters. PR [#1534](https://github.com/tiangolo/fastapi/pull/1534) by [@retnikt](https://github.com/retnikt).
* When using Pydantic models with `__root__`, use the internal value in `jsonable_encoder`. PR [#1524](https://github.com/tiangolo/fastapi/pull/1524) by [@patrickkwang](https://github.com/patrickkwang).
* Update docs for path parameters. PR [#1521](https://github.com/tiangolo/fastapi/pull/1521) by [@yankeexe](https://github.com/yankeexe).
* Update docs for first steps, links and rewording. PR [#1518](https://github.com/tiangolo/fastapi/pull/1518) by [@yankeexe](https://github.com/yankeexe).
* Enable `showCommonExtensions` in Swagger UI to show additional validations like `maxLength`, etc. PR [#1466](https://github.com/tiangolo/fastapi/pull/1466) by [@TiewKH](https://github.com/TiewKH).
* Make `OAuth2PasswordRequestFormStrict` importable directly from `fastapi.security`. PR [#1462](https://github.com/tiangolo/fastapi/pull/1462) by [@RichardHoekstra](https://github.com/RichardHoekstra).
* Add docs about [Default response class](https://fastapi.tiangolo.com/advanced/custom-response/#default-response-class). PR [#1455](https://github.com/tiangolo/fastapi/pull/1455) by [@TezRomacH](https://github.com/TezRomacH).
* Add note in docs about additional parameters `response_model_exclude_defaults` and `response_model_exclude_none` in [Response Model](https://fastapi.tiangolo.com/tutorial/response-model/#use-the-response_model_exclude_unset-parameter). PR [#1427](https://github.com/tiangolo/fastapi/pull/1427) by [@wshayes](https://github.com/wshayes).
* Add note about [PyCharm Pydantic plugin](https://github.com/koxudaxi/pydantic-pycharm-plugin) to docs. PR [#1420](https://github.com/tiangolo/fastapi/pull/1420) by [@koxudaxi](https://github.com/koxudaxi).
* Update and clarify testing function name. PR [#1395](https://github.com/tiangolo/fastapi/pull/1395) by [@chenl](https://github.com/chenl).
* Fix duplicated headers created by indirect dependencies that use the request directly. PR [#1386](https://github.com/tiangolo/fastapi/pull/1386) by [@obataku](https://github.com/obataku) from tests by [@scottsmith2gmail](https://github.com/scottsmith2gmail).
* Upgrade Starlette version to `0.13.4`. PR [#1361](https://github.com/tiangolo/fastapi/pull/1361) by [@rushton](https://github.com/rushton).
* Improve error handling and feedback for requests with invalid JSON. PR [#1354](https://github.com/tiangolo/fastapi/pull/1354) by [@aviramha](https://github.com/aviramha).
* Add support for declaring metadata for tags in OpenAPI. New docs at [Tutorial - Metadata and Docs URLs - Metadata for tags](https://fastapi.tiangolo.com/tutorial/metadata/#metadata-for-tags). PR [#1348](https://github.com/tiangolo/fastapi/pull/1348) by [@thomas-maschler](https://github.com/thomas-maschler).
* Add basic setup for Russian translations. PR [#1566](https://github.com/tiangolo/fastapi/pull/1566).
* Remove obsolete Chinese articles after adding official community translations. PR [#1510](https://github.com/tiangolo/fastapi/pull/1510) by [@waynerv](https://github.com/waynerv).
* Add `__repr__` for *path operation function* parameter helpers (like `Query`, `Depends`, etc) to simplify debugging. PR [#1560](https://github.com/tiangolo/fastapi/pull/1560) by [@rkbeatss](https://github.com/rkbeatss) and [@victorphoenix3](https://github.com/victorphoenix3).

## 0.56.1 (2020-06-12)

* Add link to advanced docs from tutorial. PR [#1512](https://github.com/tiangolo/fastapi/pull/1512) by [@kx-chen](https://github.com/kx-chen).
* Remove internal unnecessary f-strings. PR [#1526](https://github.com/tiangolo/fastapi/pull/1526) by [@kotamatsuoka](https://github.com/kotamatsuoka).
* Add translation to Chinese for [Query Parameters and String Validations - 查询参数和字符串校验](https://fastapi.tiangolo.com/zh/tutorial/query-params-str-validations/). PR [#1500](https://github.com/tiangolo/fastapi/pull/1500) by [@waynerv](https://github.com/waynerv).
* Add translation to Chinese for [Request Body - 请求体](https://fastapi.tiangolo.com/zh/tutorial/body/). PR [#1492](https://github.com/tiangolo/fastapi/pull/1492) by [@waynerv](https://github.com/waynerv).
* Add translation to Chinese for [Help FastAPI - Get Help - 帮助 FastAPI - 获取帮助](https://fastapi.tiangolo.com/zh/help-fastapi/). PR [#1465](https://github.com/tiangolo/fastapi/pull/1465) by [@waynerv](https://github.com/waynerv).
* Add translation to Chinese for [Query Parameters - 查询参数](https://fastapi.tiangolo.com/zh/tutorial/query-params/). PR [#1454](https://github.com/tiangolo/fastapi/pull/1454) by [@waynerv](https://github.com/waynerv).
* Add translation to Chinese for [Contributing - 开发 - 贡献](https://fastapi.tiangolo.com/zh/contributing/). PR [#1460](https://github.com/tiangolo/fastapi/pull/1460) by [@waynerv](https://github.com/waynerv).
* Add translation to Chinese for [Path Parameters - 路径参数](https://fastapi.tiangolo.com/zh/tutorial/path-params/). PR [#1453](https://github.com/tiangolo/fastapi/pull/1453) by [@waynerv](https://github.com/waynerv).
* Add official Microsoft project generator for [serving spaCy with FastAPI and Azure Cognitive Skills](https://github.com/microsoft/cookiecutter-spacy-fastapi) to [Project Generators](https://fastapi.tiangolo.com/project-generation/). PR [#1390](https://github.com/tiangolo/fastapi/pull/1390) by [@kabirkhan](https://github.com/kabirkhan).
* Update docs in [Python Types Intro](https://fastapi.tiangolo.com/python-types/) to include info about `Optional`. Original PR [#1377](https://github.com/tiangolo/fastapi/pull/1377) by [@yaegassy](https://github.com/yaegassy).
* Fix support for callable class dependencies with `yield`. PR [#1365](https://github.com/tiangolo/fastapi/pull/1365) by [@mrosales](https://github.com/mrosales).
* Fix/remove incorrect error logging when a client sends invalid payloads. PR [#1351](https://github.com/tiangolo/fastapi/pull/1351) by [@dbanty](https://github.com/dbanty).
* Add translation to Chinese for [First Steps - 第一步](https://fastapi.tiangolo.com/zh/tutorial/first-steps/). PR [#1323](https://github.com/tiangolo/fastapi/pull/1323) by [@waynerv](https://github.com/waynerv).
* Fix generating OpenAPI for apps using callbacks with routers including Pydantic models. PR [#1322](https://github.com/tiangolo/fastapi/pull/1322) by [@nsidnev](https://github.com/nsidnev).
* Optimize internal regex performance in `get_path_param_names()`. PR [#1243](https://github.com/tiangolo/fastapi/pull/1243) by [@heckad](https://github.com/heckad).
* Remove `*,` from functions in docs where it's not needed. PR [#1239](https://github.com/tiangolo/fastapi/pull/1239) by [@pankaj-giri](https://github.com/pankaj-giri).
* Start translations for Italian. PR [#1557](https://github.com/tiangolo/fastapi/pull/1557) by [@csr](https://github.com/csr).

## 0.56.0 (2020-06-11)

* Add support for ASGI `root_path`:
    * Use `root_path` internally for mounted applications, so that OpenAPI and the docs UI works automatically without extra configurations and parameters.
    * Add new `root_path` parameter for `FastAPI` applications to provide it in cases where it can be set with the command line (e.g. for Uvicorn and Hypercorn, with the parameter `--root-path`).
    * Deprecate `openapi_prefix` parameter in favor of the new `root_path` parameter.
    * Add new/updated docs for [Sub Applications - Mounts](https://fastapi.tiangolo.com/advanced/sub-applications/), without `openapi_prefix` (as it is now handled automatically).
    * Add new/updated docs for [Behind a Proxy](https://fastapi.tiangolo.com/advanced/behind-a-proxy/), including how to setup a local testing proxy with Traefik and using `root_path`.
    * Update docs for [Extending OpenAPI](https://fastapi.tiangolo.com/advanced/extending-openapi/) with the new `openapi_prefix` parameter passed (internally generated from `root_path`).
    * Original PR [#1199](https://github.com/tiangolo/fastapi/pull/1199) by [@iksteen](https://github.com/iksteen).
* Update new issue templates and docs: [Help FastAPI - Get Help](https://fastapi.tiangolo.com/help-fastapi/). PR [#1531](https://github.com/tiangolo/fastapi/pull/1531).
* Update GitHub action issue-manager. PR [#1520](https://github.com/tiangolo/fastapi/pull/1520).
* Add new links:
    * **English articles**:
        * [Real-time Notifications with Python and Postgres](https://wuilly.com/2019/10/real-time-notifications-with-python-and-postgres/) by [Guillermo Cruz](https://wuilly.com/).
        * [Microservice in Python using FastAPI](https://dev.to/paurakhsharma/microservice-in-python-using-fastapi-24cc)  by [Paurakh Sharma Humagain](https://x.com/PaurakhSharma).
        * [Build simple API service with Python FastAPI — Part 1](https://dev.to/cuongld2/build-simple-api-service-with-python-fastapi-part-1-581o) by [cuongld2](https://dev.to/cuongld2).
        * [FastAPI + Zeit.co = 🚀](https://paulsec.github.io/posts/fastapi_plus_zeit_serverless_fu/) by [Paul Sec](https://x.com/PaulWebSec).
        * [Build a web API from scratch with FastAPI - the workshop](https://dev.to/tiangolo/build-a-web-api-from-scratch-with-fastapi-the-workshop-2ehe) by [Sebastián Ramírez (tiangolo)](https://x.com/tiangolo).
        * [Build a Secure Twilio Webhook with Python and FastAPI](https://www.twilio.com/blog/build-secure-twilio-webhook-python-fastapi)  by [Twilio](https://www.twilio.com).
        * [Using FastAPI with Django](https://www.stavros.io/posts/fastapi-with-django/)  by [Stavros Korokithakis](https://x.com/Stavros).
        * [Introducing Dispatch](https://netflixtechblog.com/introducing-dispatch-da4b8a2a8072) by [Netflix](https://netflixtechblog.com/).
    * **Podcasts**:
        * [Build The Next Generation Of Python Web Applications With FastAPI - Episode 259 - interview to Sebastían Ramírez (tiangolo)](https://www.pythonpodcast.com/fastapi-web-application-framework-episode-259/) by [Podcast.`__init__`](https://www.pythonpodcast.com/).
    * **Talks**:
        * [PyConBY 2020: Serve ML models easily with FastAPI](https://www.youtube.com/watch?v=z9K5pwb0rt8) by [Sebastián Ramírez (tiangolo)](https://x.com/tiangolo).
        * [[VIRTUAL] Py.Amsterdam's flying Software Circus: Intro to FastAPI](https://www.youtube.com/watch?v=PnpTY1f4k2U) by [Sebastián Ramírez (tiangolo)](https://x.com/tiangolo).
    * PR [#1467](https://github.com/tiangolo/fastapi/pull/1467).
* Add translation to Chinese for [Python Types Intro - Python 类型提示简介](https://fastapi.tiangolo.com/zh/python-types/). PR [#1197](https://github.com/tiangolo/fastapi/pull/1197) by [@waynerv](https://github.com/waynerv).

## 0.55.1 (2020-05-23)

* Fix handling of enums with their own schema in path parameters. To support [pydantic/pydantic#1432](https://github.com/pydantic/pydantic/pull/1432) in FastAPI. PR [#1463](https://github.com/tiangolo/fastapi/pull/1463).

## 0.55.0 (2020-05-23)

* Allow enums to allow them to have their own schemas in OpenAPI. To support [pydantic/pydantic#1432](https://github.com/pydantic/pydantic/pull/1432) in FastAPI. PR [#1461](https://github.com/tiangolo/fastapi/pull/1461).
* Add links for funding through [GitHub sponsors](https://github.com/sponsors/tiangolo). PR [#1425](https://github.com/tiangolo/fastapi/pull/1425).
* Update issue template for for questions. PR [#1344](https://github.com/tiangolo/fastapi/pull/1344) by [@retnikt](https://github.com/retnikt).
* Update warning about storing passwords in docs. PR [#1336](https://github.com/tiangolo/fastapi/pull/1336) by [@skorokithakis](https://github.com/skorokithakis).
* Fix typo. PR [#1326](https://github.com/tiangolo/fastapi/pull/1326) by [@chenl](https://github.com/chenl).
* Add translation to Portuguese for [Alternatives, Inspiration and Comparisons - Alternativas, Inspiração e Comparações](https://fastapi.tiangolo.com/pt/alternatives/). PR [#1325](https://github.com/tiangolo/fastapi/pull/1325) by [@Serrones](https://github.com/Serrones).
* Fix 2 typos in docs. PR [#1324](https://github.com/tiangolo/fastapi/pull/1324) by [@waynerv](https://github.com/waynerv).
* Update CORS docs, fix correct default of `max_age=600`. PR [#1301](https://github.com/tiangolo/fastapi/pull/1301) by [@derekbekoe](https://github.com/derekbekoe).
* Add translation of [main page to Portuguese](https://fastapi.tiangolo.com/pt/). PR [#1300](https://github.com/tiangolo/fastapi/pull/1300) by [@Serrones](https://github.com/Serrones).
* Re-word and clarify docs for extra info in fields. PR [#1299](https://github.com/tiangolo/fastapi/pull/1299) by [@chris-allnutt](https://github.com/chris-allnutt).
* Make sure the `*` in short features in the docs is consistent (after `.`) in all languages. PR [#1424](https://github.com/tiangolo/fastapi/pull/1424).
* Update order of execution for `get_db` in SQLAlchemy tutorial. PR [#1293](https://github.com/tiangolo/fastapi/pull/1293) by [@bcb](https://github.com/bcb).
* Fix typos in Async docs. PR [#1423](https://github.com/tiangolo/fastapi/pull/1423).

## 0.54.2 (2020-05-16)

* Add translation to Spanish for [Concurrency and async / await - Concurrencia y async / await](https://fastapi.tiangolo.com/es/async/). PR [#1290](https://github.com/tiangolo/fastapi/pull/1290) by [@alvaropernas](https://github.com/alvaropernas).
* Remove obsolete vote link. PR [#1289](https://github.com/tiangolo/fastapi/pull/1289) by [@donhui](https://github.com/donhui).
* Allow disabling docs UIs by just disabling OpenAPI with `openapi_url=None`. New example in docs: [Advanced: Conditional OpenAPI](https://fastapi.tiangolo.com/advanced/conditional-openapi/). PR [#1421](https://github.com/tiangolo/fastapi/pull/1421).
* Add translation to Portuguese for [Benchmarks - Comparações](https://fastapi.tiangolo.com/pt/benchmarks/). PR [#1274](https://github.com/tiangolo/fastapi/pull/1274) by [@Serrones](https://github.com/Serrones).
* Add translation to Portuguese for [Tutorial - User Guide - Intro - Tutorial - Guia de Usuário - Introdução](https://fastapi.tiangolo.com/pt/tutorial/). PR [#1259](https://github.com/tiangolo/fastapi/pull/1259) by [@marcosmmb](https://github.com/marcosmmb).
* Allow using Unicode in MkDocs for translations. PR [#1419](https://github.com/tiangolo/fastapi/pull/1419).
* Add translation to Spanish for [Advanced User Guide - Intro - Guía de Usuario Avanzada - Introducción](https://fastapi.tiangolo.com/es/advanced/). PR [#1250](https://github.com/tiangolo/fastapi/pull/1250) by [@jfunez](https://github.com/jfunez).
* Add translation to Portuguese for [History, Design and Future - História, Design e Futuro](https://fastapi.tiangolo.com/pt/history-design-future/). PR [#1249](https://github.com/tiangolo/fastapi/pull/1249) by [@marcosmmb](https://github.com/marcosmmb).
* Add translation to Portuguese for [Features - Recursos](https://fastapi.tiangolo.com/pt/features/). PR [#1248](https://github.com/tiangolo/fastapi/pull/1248) by [@marcosmmb](https://github.com/marcosmmb).
* Add translation to Spanish for [Tutorial - User Guide - Intro - Tutorial - Guía de Usuario - Introducción](https://fastapi.tiangolo.com/es/tutorial/). PR [#1244](https://github.com/tiangolo/fastapi/pull/1244) by [@MartinEliasQ](https://github.com/MartinEliasQ).
* Add translation to Chinese for [Deployment - 部署](https://fastapi.tiangolo.com/zh/deployment/). PR [#1203](https://github.com/tiangolo/fastapi/pull/1203) by [@RunningIkkyu](https://github.com/RunningIkkyu).
* Add translation to Chinese for [Tutorial - User Guide - Intro - 教程 - 用户指南 - 简介](https://fastapi.tiangolo.com/zh/tutorial/). PR [#1202](https://github.com/tiangolo/fastapi/pull/1202) by [@waynerv](https://github.com/waynerv).
* Add translation to Chinese for [Features - 特性](https://fastapi.tiangolo.com/zh/features/). PR [#1192](https://github.com/tiangolo/fastapi/pull/1192) by [@Dustyposa](https://github.com/Dustyposa).
* Add translation for [main page to Chinese](https://fastapi.tiangolo.com/zh/) PR [#1191](https://github.com/tiangolo/fastapi/pull/1191) by [@waynerv](https://github.com/waynerv).
* Update docs for project generation. PR [#1287](https://github.com/tiangolo/fastapi/pull/1287).
* Add Spanish translation for [Introducción a los Tipos de Python (Python Types Intro)](https://fastapi.tiangolo.com/es/python-types/). PR [#1237](https://github.com/tiangolo/fastapi/pull/1237) by [@mariacamilagl](https://github.com/mariacamilagl).
* Add Spanish translation for [Características (Features)](https://fastapi.tiangolo.com/es/features/). PR [#1220](https://github.com/tiangolo/fastapi/pull/1220) by [@mariacamilagl](https://github.com/mariacamilagl).

## 0.54.1 (2020-04-08)

* Update database test setup. PR [#1226](https://github.com/tiangolo/fastapi/pull/1226).
* Improve test debugging by showing response text in failing tests. PR [#1222](https://github.com/tiangolo/fastapi/pull/1222) by [@samuelcolvin](https://github.com/samuelcolvin).

## 0.54.0 (2020-04-05)

* Fix grammatical mistakes in async docs. PR [#1188](https://github.com/tiangolo/fastapi/pull/1188) by [@mickeypash](https://github.com/mickeypash).
* Add support for `response_model_exclude_defaults` and `response_model_exclude_none`:
    * Deprecate the parameter `include_none` in `jsonable_encoder` and add the inverted `exclude_none`, to keep in sync with Pydantic.
    * PR [#1166](https://github.com/tiangolo/fastapi/pull/1166) by [@voegtlel](https://github.com/voegtlel).
* Add example about [Testing a Database](https://fastapi.tiangolo.com/advanced/testing-database/). Initial PR [#1144](https://github.com/tiangolo/fastapi/pull/1144) by [@duganchen](https://github.com/duganchen).
* Update docs for [Development - Contributing: Translations](https://fastapi.tiangolo.com/contributing/#translations) including note about reviewing translation PRs. [#1215](https://github.com/tiangolo/fastapi/pull/1215).
* Update log style in README.md for GitHub Markdown compatibility. PR [#1200](https://github.com/tiangolo/fastapi/pull/1200) by [#geekgao](https://github.com/geekgao).
* Add Python venv `env` to `.gitignore`. PR [#1212](https://github.com/tiangolo/fastapi/pull/1212) by [@cassiobotaro](https://github.com/cassiobotaro).
* Start Portuguese translations. PR [#1210](https://github.com/tiangolo/fastapi/pull/1210) by [@cassiobotaro](https://github.com/cassiobotaro).
* Update docs for Pydantic's `Settings` using a dependency with `@lru_cache()`. PR [#1214](https://github.com/tiangolo/fastapi/pull/1214).
* Add first translation to Spanish [FastAPI](https://fastapi.tiangolo.com/es/). PR [#1201](https://github.com/tiangolo/fastapi/pull/1201) by [@mariacamilagl](https://github.com/mariacamilagl).
* Add docs about [Settings and Environment Variables](https://fastapi.tiangolo.com/advanced/settings/). Initial PR [1118](https://github.com/tiangolo/fastapi/pull/1118) by [@alexmitelman](https://github.com/alexmitelman).

## 0.53.2 (2020-03-30)

* Fix automatic embedding of body fields for dependencies and sub-dependencies. Original PR [#1079](https://github.com/tiangolo/fastapi/pull/1079) by [@Toad2186](https://github.com/Toad2186).
* Fix dependency overrides in WebSocket testing. PR [#1122](https://github.com/tiangolo/fastapi/pull/1122) by [@amitlissack](https://github.com/amitlissack).
* Fix docs script to ensure languages are always sorted. PR [#1189](https://github.com/tiangolo/fastapi/pull/1189).
* Start translations for Chinese. PR [#1187](https://github.com/tiangolo/fastapi/pull/1187) by [@RunningIkkyu](https://github.com/RunningIkkyu).
* Add docs for [Schema Extra - Example](https://fastapi.tiangolo.com/tutorial/schema-extra-example/). PR [#1185](https://github.com/tiangolo/fastapi/pull/1185).

## 0.53.1 (2020-03-29)

* Fix included example after translations refactor. PR [#1182](https://github.com/tiangolo/fastapi/pull/1182).
* Add docs example for `example` in `Field`. Docs at [Body - Fields: JSON Schema extras](https://fastapi.tiangolo.com/tutorial/body-fields/#json-schema-extras). PR [#1106](https://github.com/tiangolo/fastapi/pull/1106) by [@JohnPaton](https://github.com/JohnPaton).
* Fix using recursive models in `response_model`. PR [#1164](https://github.com/tiangolo/fastapi/pull/1164) by [@voegtlel](https://github.com/voegtlel).
* Add docs for [Pycharm Debugging](https://fastapi.tiangolo.com/tutorial/debugging/). PR [#1096](https://github.com/tiangolo/fastapi/pull/1096) by [@youngquan](https://github.com/youngquan).
* Fix typo in docs. PR [#1148](https://github.com/tiangolo/fastapi/pull/1148) by [@PLNech](https://github.com/PLNech).
* Update Windows development environment instructions. PR [#1179](https://github.com/tiangolo/fastapi/pull/1179).

## 0.53.0 (2020-03-27)

* Update test coverage badge. PR [#1175](https://github.com/tiangolo/fastapi/pull/1175).
* Add `orjson` to `pip install fastapi[all]`. PR [#1161](https://github.com/tiangolo/fastapi/pull/1161) by [@michael0liver](https://github.com/michael0liver).
* Fix included example for `GZipMiddleware`. PR [#1138](https://github.com/tiangolo/fastapi/pull/1138) by [@arimbr](https://github.com/arimbr).
* Fix class name in docstring for `OAuth2PasswordRequestFormStrict`. PR [#1126](https://github.com/tiangolo/fastapi/pull/1126) by [@adg-mh](https://github.com/adg-mh).
* Clarify function name in example in docs. PR [#1121](https://github.com/tiangolo/fastapi/pull/1121) by [@tmsick](https://github.com/tmsick).
* Add external link [Apache Kafka producer and consumer with FastAPI and aiokafka](https://iwpnd.pw/articles/2020-03/apache-kafka-fastapi-geostream) to docs. PR [#1112](https://github.com/tiangolo/fastapi/pull/1112) by [@iwpnd](https://github.com/iwpnd).
* Fix serialization when using `by_alias` or `exclude_unset` and returning data with Pydantic models. PR [#1074](https://github.com/tiangolo/fastapi/pull/1074) by [@juhovh-aiven](https://github.com/juhovh-aiven).
* Add Gitter chat to docs. PR [#1061](https://github.com/tiangolo/fastapi/pull/1061) by [@aakashnand](https://github.com/aakashnand).
* Update and simplify translations docs. PR [#1171](https://github.com/tiangolo/fastapi/pull/1171).
* Update development of FastAPI docs, set address to `127.0.0.1` to improve Windows support. PR [#1169](https://github.com/tiangolo/fastapi/pull/1169) by [@mariacamilagl](https://github.com/mariacamilagl).
* Add support for docs translations. New docs: [Development - Contributing: Docs: Translations](https://fastapi.tiangolo.com/contributing/#translations). PR [#1168](https://github.com/tiangolo/fastapi/pull/1168).
* Update terminal styles in docs and add note about [**Typer**, the FastAPI of CLIs](https://typer.tiangolo.com/). PR [#1139](https://github.com/tiangolo/fastapi/pull/1139).

## 0.52.0 (2020-03-01)

* Add new high-performance JSON response class using `orjson`. New docs: [Custom Response - HTML, Stream, File, others: `ORJSONResponse`](https://fastapi.tiangolo.com/advanced/custom-response/#use-orjsonresponse). PR [#1065](https://github.com/tiangolo/fastapi/pull/1065).

## 0.51.0 (2020-03-01)

* Re-export utils from Starlette:
    * This allows using things like `from fastapi.responses import JSONResponse` instead of `from starlette.responses import JSONResponse`.
    * It's mainly syntax sugar, a convenience for developer experience.
    * Now `Request`, `Response`, `WebSocket`, `status` can be imported directly from `fastapi` as in `from fastapi import Response`. This is because those are frequently used, to use the request directly, to set headers and cookies, to get status codes, etc.
    * Documentation changes in many places, but new docs and noticeable improvements:
        * [Custom Response - HTML, Stream, File, others](https://fastapi.tiangolo.com/advanced/custom-response/).
        * [Advanced Middleware](https://fastapi.tiangolo.com/advanced/middleware/).
        * [Including WSGI - Flask, Django, others](https://fastapi.tiangolo.com/advanced/wsgi/).
    * PR [#1064](https://github.com/tiangolo/fastapi/pull/1064).

## 0.50.0 (2020-02-29)

* Add link to Release Notes from docs about pinning versions for deployment. PR [#1058](https://github.com/tiangolo/fastapi/pull/1058).
* Upgrade code to use the latest version of Starlette, including:
    * Several bug fixes.
    * Optional redirects of slashes, with or without ending in `/`.
    * Events for routers, `"startup"`, and `"shutdown"`.
    * PR [#1057](https://github.com/tiangolo/fastapi/pull/1057).
* Add docs about pinning FastAPI versions for deployment: [Deployment: FastAPI versions](https://fastapi.tiangolo.com/deployment/#fastapi-versions). PR [#1056](https://github.com/tiangolo/fastapi/pull/1056).

## 0.49.2 (2020-02-29)

* Fix links in release notes. PR [#1052](https://github.com/tiangolo/fastapi/pull/1052) by [@sattosan](https://github.com/sattosan).
* Fix typo in release notes. PR [#1051](https://github.com/tiangolo/fastapi/pull/1051) by [@sattosan](https://github.com/sattosan).
* Refactor/clarify `serialize_response` parameter name to avoid confusion. PR [#1031](https://github.com/tiangolo/fastapi/pull/1031) by [@patrickmckenna](https://github.com/patrickmckenna).
* Refactor calling each a path operation's handler function in an isolated function, to simplify profiling. PR [#1027](https://github.com/tiangolo/fastapi/pull/1027) by [@sm-Fifteen](https://github.com/sm-Fifteen).
* Add missing dependencies for testing. PR [#1026](https://github.com/tiangolo/fastapi/pull/1026) by [@sm-Fifteen](https://github.com/sm-Fifteen).
* Fix accepting valid types for response models, including Python types like `List[int]`. PR [#1017](https://github.com/tiangolo/fastapi/pull/1017) by [@patrickmckenna](https://github.com/patrickmckenna).
* Fix format in SQL tutorial. PR [#1015](https://github.com/tiangolo/fastapi/pull/1015) by [@vegarsti](https://github.com/vegarsti).

## 0.49.1 (2020-02-28)

* Fix path operation duplicated parameters when used in dependencies and the path operation function. PR [#994](https://github.com/tiangolo/fastapi/pull/994) by [@merowinger92](https://github.com/merowinger92).
* Update Netlify previews deployment GitHub action as the fix is already merged and there's a new release. PR [#1047](https://github.com/tiangolo/fastapi/pull/1047).
* Move mypy configurations to config file. PR [#987](https://github.com/tiangolo/fastapi/pull/987) by [@hukkinj1](https://github.com/hukkinj1).
* Temporary fix to Netlify previews not deployable from PRs from forks. PR [#1046](https://github.com/tiangolo/fastapi/pull/1046) by [@mariacamilagl](https://github.com/mariacamilagl).

## 0.49.0 (2020-02-16)

* Fix encoding of `pathlib` paths in `jsonable_encoder`. PR [#978](https://github.com/tiangolo/fastapi/pull/978) by [@patrickmckenna](https://github.com/patrickmckenna).
* Add articles to [External Links](https://fastapi.tiangolo.com/external-links/): [PythonのWeb frameworkのパフォーマンス比較 (Django, Flask, responder, FastAPI, japronto)](https://qiita.com/bee2/items/0ad260ab9835a2087dae) and [[FastAPI] Python製のASGI Web フレームワーク FastAPIに入門する](https://qiita.com/bee2/items/75d9c0d7ba20e7a4a0e9). PR [#974](https://github.com/tiangolo/fastapi/pull/974) by [@tokusumi](https://github.com/tokusumi).
* Fix broken links in docs. PR [#949](https://github.com/tiangolo/fastapi/pull/949) by [@tsotnikov](https://github.com/tsotnikov).
* Fix small typos. PR [#941](https://github.com/tiangolo/fastapi/pull/941) by [@NikitaKolesov](https://github.com/NikitaKolesov).
* Update and clarify docs for dependencies with `yield`. PR [#986](https://github.com/tiangolo/fastapi/pull/986).
* Add Mermaid JS support for diagrams in docs. Add first diagrams to [Dependencies: First Steps](https://fastapi.tiangolo.com/tutorial/dependencies/) and [Dependencies with `yield` and `HTTPException`](https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/#dependencies-with-yield-and-httpexception). PR [#985](https://github.com/tiangolo/fastapi/pull/985).
* Update CI to run docs deployment in GitHub actions. PR [#983](https://github.com/tiangolo/fastapi/pull/983).
* Allow `callable`s in *path operation functions*, like functions modified with `functools.partial`. PR [#977](https://github.com/tiangolo/fastapi/pull/977).

## 0.48.0 (2020-02-04)

* Run linters first in tests to error out faster. PR [#948](https://github.com/tiangolo/fastapi/pull/948).
* Log warning about `email-validator` only when used. PR [#946](https://github.com/tiangolo/fastapi/pull/946).
* Simplify [Peewee docs](https://fastapi.tiangolo.com/advanced/sql-databases-peewee/) with double dependency with `yield`. PR [#947](https://github.com/tiangolo/fastapi/pull/947).
* Add article [External Links](https://fastapi.tiangolo.com/external-links/): [Create and Deploy FastAPI app to Heroku](https://www.tutlinks.com/create-and-deploy-fastapi-app-to-heroku/). PR [#942](https://github.com/tiangolo/fastapi/pull/942) by [@windson](https://github.com/windson).
* Update description of Sanic, as it is now ASGI too. PR [#932](https://github.com/tiangolo/fastapi/pull/932) by [@raphaelauv](https://github.com/raphaelauv).
* Fix typo in main page. PR [#920](https://github.com/tiangolo/fastapi/pull/920) by [@mMarzeta](https://github.com/mMarzeta).
* Fix parsing of possibly invalid bodies. PR [#918](https://github.com/tiangolo/fastapi/pull/918) by [@dmontagu](https://github.com/dmontagu).
* Fix typo [#916](https://github.com/tiangolo/fastapi/pull/916) by [@adursun](https://github.com/adursun).
* Allow `Any` type for enums in OpenAPI. PR [#906](https://github.com/tiangolo/fastapi/pull/906) by [@songzhi](https://github.com/songzhi).
* Add article to [External Links](https://fastapi.tiangolo.com/external-links/): [How to continuously deploy a FastAPI to AWS Lambda with AWS SAM](https://iwpnd.pw/articles/2020-01/deploy-fastapi-to-aws-lambda). PR [#901](https://github.com/tiangolo/fastapi/pull/901) by [@iwpnd](https://github.com/iwpnd).
* Add note about using Body parameters without Pydantic. PR [#900](https://github.com/tiangolo/fastapi/pull/900) by [@pawamoy](https://github.com/pawamoy).
* Fix Pydantic field clone logic. PR [#899](https://github.com/tiangolo/fastapi/pull/899) by [@deuce2367](https://github.com/deuce2367).
* Fix link in middleware docs. PR [#893](https://github.com/tiangolo/fastapi/pull/893) by [@linchiwei123](https://github.com/linchiwei123).
* Rename default API title from "Fast API" to "FastAPI" for consistency. PR [#890](https://github.com/tiangolo/fastapi/pull/890).

## 0.47.1 (2020-01-18)

* Fix model filtering in `response_model`, cloning sub-models. PR [#889](https://github.com/tiangolo/fastapi/pull/889).
* Fix FastAPI serialization of Pydantic models using ORM mode blocking the event loop. PR [#888](https://github.com/tiangolo/fastapi/pull/888).

## 0.47.0 (2020-01-18)

* Refactor documentation to make a simpler and shorter [Tutorial - User Guide](https://fastapi.tiangolo.com/tutorial/) and an additional [Advanced User Guide](https://fastapi.tiangolo.com/advanced/) with all the additional docs. PR [#887](https://github.com/tiangolo/fastapi/pull/887).
* Tweak external links, Markdown format, typos. PR [#881](https://github.com/tiangolo/fastapi/pull/881).
* Fix bug in tutorial handling HTTP Basic Auth `username` and `password`. PR [#865](https://github.com/tiangolo/fastapi/pull/865) by [@isaevpd](https://github.com/isaevpd).
* Fix handling form *path operation* parameters declared with pure classes like `list`, `tuple`, etc. PR [#856](https://github.com/tiangolo/fastapi/pull/856) by [@nsidnev](https://github.com/nsidnev).
* Add request `body` to `RequestValidationError`, new docs: [Use the `RequestValidationError` body](https://fastapi.tiangolo.com/tutorial/handling-errors/#use-the-requestvalidationerror-body). Initial PR [#853](https://github.com/tiangolo/fastapi/pull/853) by [@aviramha](https://github.com/aviramha).
* Update [External Links](https://fastapi.tiangolo.com/external-links/) with new links and dynamic GitHub projects with `fastapi` topic. PR [#850](https://github.com/tiangolo/fastapi/pull/850).
* Fix Peewee `contextvars` handling in docs: [SQL (Relational) Databases with Peewee](https://fastapi.tiangolo.com/advanced/sql-databases-peewee/). PR [#879](https://github.com/tiangolo/fastapi/pull/879).
* Setup development environment with Python's Venv and Flit, instead of requiring the extra Pipenv duplicating dependencies. Updated docs: [Development - Contributing](https://fastapi.tiangolo.com/contributing/). PR [#877](https://github.com/tiangolo/fastapi/pull/877).
* Update docs for [HTTP Basic Auth](https://fastapi.tiangolo.com/advanced/security/http-basic-auth/) to improve security against timing attacks. Initial PR [#807](https://github.com/tiangolo/fastapi/pull/807) by [@zwass](https://github.com/zwass).

## 0.46.0 (2020-01-08)

* Fix typos and tweak configs. PR [#837](https://github.com/tiangolo/fastapi/pull/837).
* Add link to Chinese article in [External Links](https://fastapi.tiangolo.com/external-links/). PR [810](https://github.com/tiangolo/fastapi/pull/810) by [@wxq0309](https://github.com/wxq0309).
* Implement `OAuth2AuthorizationCodeBearer` class. PR [#797](https://github.com/tiangolo/fastapi/pull/797) by [@kuwv](https://github.com/kuwv).
* Update example upgrade in docs main page. PR [#795](https://github.com/tiangolo/fastapi/pull/795) by [@cdeil](https://github.com/cdeil).
* Fix callback handling for sub-routers. PR [#792](https://github.com/tiangolo/fastapi/pull/792) by [@jekirl](https://github.com/jekirl).
* Fix typos. PR [#784](https://github.com/tiangolo/fastapi/pull/784) by [@kkinder](https://github.com/kkinder).
* Add 4 Japanese articles to [External Links](https://fastapi.tiangolo.com/external-links/). PR [#783](https://github.com/tiangolo/fastapi/pull/783) by [@HymanZHAN](https://github.com/HymanZHAN).
* Add support for subtypes of main types in `jsonable_encoder`, e.g. asyncpg's UUIDs. PR [#756](https://github.com/tiangolo/fastapi/pull/756) by [@RmStorm](https://github.com/RmStorm).
* Fix usage of Pydantic's `HttpUrl` in docs. PR [#832](https://github.com/tiangolo/fastapi/pull/832) by [@Dustyposa](https://github.com/Dustyposa).
* Fix Twitter links in docs. PR [#813](https://github.com/tiangolo/fastapi/pull/813) by [@justindujardin](https://github.com/justindujardin).
* Add docs for correctly [using FastAPI with Peewee ORM](https://fastapi.tiangolo.com/advanced/sql-databases-peewee/). Including how to overwrite parts of Peewee to correctly handle async threads. PR [#789](https://github.com/tiangolo/fastapi/pull/789).

## 0.45.0 (2019-12-11)

* Add support for OpenAPI Callbacks:
    * New docs: [OpenAPI Callbacks](https://fastapi.tiangolo.com/advanced/openapi-callbacks/).
    * Refactor generation of `operationId`s to be valid Python names (also valid variables in most languages).
    * Add `default_response_class` parameter to `APIRouter`.
    * Original PR [#722](https://github.com/tiangolo/fastapi/pull/722) by [@booooh](https://github.com/booooh).
* Refactor logging to use the same logger everywhere, update log strings and levels. PR [#781](https://github.com/tiangolo/fastapi/pull/781).
* Add article to [External Links](https://fastapi.tiangolo.com/external-links/): [Почему Вы должны попробовать FastAPI?](https://habr.com/ru/post/478620/). PR [#766](https://github.com/tiangolo/fastapi/pull/766) by [@prostomarkeloff](https://github.com/prostomarkeloff).
* Remove gender bias in docs for handling errors. PR [#780](https://github.com/tiangolo/fastapi/pull/780). Original idea in PR [#761](https://github.com/tiangolo/fastapi/pull/761) by [@classywhetten](https://github.com/classywhetten).
* Rename docs and references to `body-schema` to `body-fields` to keep in line with Pydantic. PR [#746](https://github.com/tiangolo/fastapi/pull/746) by [@prostomarkeloff](https://github.com/prostomarkeloff).

## 0.44.1 (2019-12-04)

* Add GitHub social preview images to git. PR [#752](https://github.com/tiangolo/fastapi/pull/752).
* Update PyPI "trove classifiers". PR [#751](https://github.com/tiangolo/fastapi/pull/751).
* Add full support for Python 3.8. Enable Python 3.8 in full in Travis. PR [749](https://github.com/tiangolo/fastapi/pull/749).
* Update "new issue" templates. PR [#749](https://github.com/tiangolo/fastapi/pull/749).
* Fix serialization of errors for exotic Pydantic types. PR [#748](https://github.com/tiangolo/fastapi/pull/748) by [@dmontagu](https://github.com/dmontagu).

## 0.44.0 (2019-11-27)

* Add GitHub action [Issue Manager](https://github.com/tiangolo/issue-manager). PR [#742](https://github.com/tiangolo/fastapi/pull/742).
* Fix typos in docs. PR [734](https://github.com/tiangolo/fastapi/pull/734) by [@bundabrg](https://github.com/bundabrg).
* Fix usage of `custom_encoder` in `jsonable_encoder`. PR [#715](https://github.com/tiangolo/fastapi/pull/715) by [@matrixise](https://github.com/matrixise).
* Fix invalid XML example. PR [710](https://github.com/tiangolo/fastapi/pull/710) by [@OcasoProtal](https://github.com/OcasoProtal).
* Fix typos and update wording in deployment docs. PR [#700](https://github.com/tiangolo/fastapi/pull/700) by [@marier-nico](https://github.com/tiangolo/fastapi/pull/700).
* Add note about dependencies in `APIRouter` docs. PR [#698](https://github.com/tiangolo/fastapi/pull/698) by [@marier-nico](https://github.com/marier-nico).
* Add support for async class methods as dependencies [#681](https://github.com/tiangolo/fastapi/pull/681) by [@frankie567](https://github.com/frankie567).
* Add FastAPI with Swagger UI cheatsheet to external links. PR [#671](https://github.com/tiangolo/fastapi/pull/671) by [@euri10](https://github.com/euri10).
* Fix typo in HTTP protocol in CORS example. PR [#647](https://github.com/tiangolo/fastapi/pull/647) by [@forestmonster](https://github.com/forestmonster).
* Add support for Pydantic versions `1.0.0` and above, with temporary (deprecated) backwards compatibility for Pydantic `0.32.2`. PR [#646](https://github.com/tiangolo/fastapi/pull/646) by [@dmontagu](https://github.com/dmontagu).

## 0.43.0 (2019-11-24)

* Update docs to reduce gender bias. PR [#645](https://github.com/tiangolo/fastapi/pull/645) by [@ticosax](https://github.com/ticosax).
* Add docs about [overriding the `operationId` for all the *path operations*](https://fastapi.tiangolo.com/advanced/path-operation-advanced-configuration/#using-the-path-operation-function-name-as-the-operationid) based on their function name. PR [#642](https://github.com/tiangolo/fastapi/pull/642) by [@SKalt](https://github.com/SKalt).
* Fix validators in models generating an incorrect key order. PR [#637](https://github.com/tiangolo/fastapi/pull/637) by [@jaddison](https://github.com/jaddison).
* Generate correct OpenAPI docs for responses with no content. PR [#621](https://github.com/tiangolo/fastapi/pull/621) by [@brotskydotcom](https://github.com/brotskydotcom).
* Remove `$` from Bash code blocks in docs for consistency. PR [#613](https://github.com/tiangolo/fastapi/pull/613) by [@nstapelbroek](https://github.com/nstapelbroek).
* Add docs for [self-serving docs' (Swagger UI) static assets](https://fastapi.tiangolo.com/advanced/extending-openapi/#self-hosting-javascript-and-css-for-docs), e.g. to use the docs offline, or without Internet. Initial PR [#557](https://github.com/tiangolo/fastapi/pull/557) by [@svalouch](https://github.com/svalouch).
* Fix `black` linting after upgrade. PR [#682](https://github.com/tiangolo/fastapi/pull/682) by [@frankie567](https://github.com/frankie567).

## 0.42.0 (2019-10-09)

* Add dependencies with `yield`, a.k.a. exit steps, context managers, cleanup, teardown, ...
    * This allows adding extra code after a dependency is done. It can be used, for example, to close database connections.
    * Dependencies with `yield` can be normal or `async`, **FastAPI** will run normal dependencies in a threadpool.
    * They can be combined with normal dependencies.
    * It's possible to have arbitrary trees/levels of dependencies with `yield` and exit steps are handled in the correct order automatically.
    * It works by default in Python 3.7 or above. For Python 3.6, it requires the extra backport dependencies:
        * `async-exit-stack`
        * `async-generator`
    * New docs at [Dependencies with `yield`](https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/).
    * Updated database docs [SQL (Relational) Databases: Main **FastAPI** app](https://fastapi.tiangolo.com/tutorial/sql-databases/#main-fastapi-app).
    * PR [#595](https://github.com/tiangolo/fastapi/pull/595).
* Fix `sitemap.xml` in website. PR [#598](https://github.com/tiangolo/fastapi/pull/598) by [@samuelcolvin](https://github.com/samuelcolvin).

## 0.41.0 (2019-10-07)

* Upgrade required Starlette to `0.12.9`, the new range is `>=0.12.9,=0.11.1,=0.28,<=0.29.0"`.
    * This adds support for Pydantic [Generic Models](https://docs.pydantic.dev/latest/#generic-models), kudos to [@dmontagu](https://github.com/dmontagu).
    * PR [#344](https://github.com/tiangolo/fastapi/pull/344).

## 0.30.1 (2019-06-28)

* Add section in docs about [External Links and Articles](https://fastapi.tiangolo.com/external-links/). PR [#341](https://github.com/tiangolo/fastapi/pull/341).

* Remove `Pipfile.lock` from the repository as it is only used by FastAPI contributors (developers of FastAPI itself). See the PR for more details. PR [#340](https://github.com/tiangolo/fastapi/pull/340).

* Update section about [Help FastAPI - Get Help](https://fastapi.tiangolo.com/help-fastapi/). PR [#339](https://github.com/tiangolo/fastapi/pull/339).

* Refine internal type declarations to improve/remove Mypy errors in users' code. PR [#338](https://github.com/tiangolo/fastapi/pull/338).

* Update and clarify [SQL tutorial with SQLAlchemy](https://fastapi.tiangolo.com/tutorial/sql-databases/). PR [#331](https://github.com/tiangolo/fastapi/pull/331) by [@mariacamilagl](https://github.com/mariacamilagl).

* Add SQLite [online viewers to the docs](https://fastapi.tiangolo.com/tutorial/sql-databases/#interact-with-the-database-directly). PR [#330](https://github.com/tiangolo/fastapi/pull/330) by [@cyrilbois](https://github.com/cyrilbois).

## 0.30.0 (2019-06-20)

* Add support for Pydantic's ORM mode:
    * Updated documentation about SQL with SQLAlchemy, using Pydantic models with ORM mode, SQLAlchemy models with relations, separation of files, simplification of code and other changes. New docs: [SQL (Relational) Databases](https://fastapi.tiangolo.com/tutorial/sql-databases/).
    * The new support for ORM mode fixes issues/adds features related to ORMs with lazy-loading, hybrid properties, dynamic/getters (using `@property` decorators) and several other use cases.
    * This applies to ORMs like SQLAlchemy, Peewee, Tortoise ORM, GINO ORM and virtually any other.
    * If your *path operations* return an arbitrary object with attributes (e.g. `my_item.name` instead of `my_item["name"]`) AND you use a `response_model`, make sure to update the Pydantic models with `orm_mode = True` as described in the docs (link above).
    * New documentation about receiving plain `dict`s as request bodies: [Bodies of arbitrary `dict`s](https://fastapi.tiangolo.com/tutorial/body-nested-models/#bodies-of-arbitrary-dicts).
    * New documentation about returning arbitrary `dict`s in responses: [Response with arbitrary `dict`](https://fastapi.tiangolo.com/tutorial/extra-models/#response-with-arbitrary-dict).
    * **Technical Details**:
        * When declaring a `response_model` it is used directly to generate the response content, from whatever was returned from the *path operation function*.
        * Before this, the return content was first passed through `jsonable_encoder` to ensure it was a "jsonable" object, like a `dict`, instead of an arbitrary object with attributes (like an ORM model). That's why you should make sure to update your Pydantic models for objects with attributes to use `orm_mode = True`.
        * If you don't have a `response_model`, the return object will still be passed through `jsonable_encoder` first.
        * When a `response_model` is declared, the same `response_model` type declaration won't be used as is, it will be "cloned" to create an new one (a cloned Pydantic `Field` with all the submodels cloned as well).
        * This avoids/fixes a potential security issue: as the returned object is passed directly to Pydantic, if the returned object was a subclass of the `response_model` (e.g. you return a `UserInDB` that inherits from `User` but contains extra fields, like `hashed_password`, and `User` is used in the `response_model`), it would still pass the validation (because `UserInDB` is a subclass of `User`) and the object would be returned as-is, including the `hashed_password`. To fix this, the declared `response_model` is cloned, if it is a Pydantic model class (or contains Pydantic model classes in it, e.g. in a `List[Item]`), the Pydantic model class(es) will be a different one (the "cloned" one). So, an object that is a subclass won't simply pass the validation and returned as-is, because it is no longer a sub-class of the cloned `response_model`. Instead, a new Pydantic model object will be created with the contents of the returned object. So, it will be a new object (made with the data from the returned one), and will be filtered by the cloned `response_model`, containing only the declared fields as normally.
    * PR [#322](https://github.com/tiangolo/fastapi/pull/322).

* Remove/clean unused RegEx code in routing. PR [#314](https://github.com/tiangolo/fastapi/pull/314) by [@dmontagu](https://github.com/dmontagu).

* Use default response status code descriptions for additional responses. PR [#313](https://github.com/tiangolo/fastapi/pull/313) by [@duxiaoyao](https://github.com/duxiaoyao).

* Upgrade Pydantic support to `0.28`. PR [#320](https://github.com/tiangolo/fastapi/pull/320) by [@jekirl](https://github.com/jekirl).

## 0.29.1 (2019-06-13)

* Fix handling an empty-body request with a required body param. PR [#311](https://github.com/tiangolo/fastapi/pull/311).

* Fix broken link in docs: [Return a Response directly](https://fastapi.tiangolo.com/advanced/response-directly/). PR [#306](https://github.com/tiangolo/fastapi/pull/306) by [@dmontagu](https://github.com/dmontagu).

* Fix docs discrepancy in docs for [Response Model](https://fastapi.tiangolo.com/tutorial/response-model/). PR [#288](https://github.com/tiangolo/fastapi/pull/288) by [@awiddersheim](https://github.com/awiddersheim).

## 0.29.0 (2019-06-06)

* Add support for declaring a `Response` parameter:
    * This allows declaring:
        * [Response Cookies](https://fastapi.tiangolo.com/advanced/response-cookies/).
        * [Response Headers](https://fastapi.tiangolo.com/advanced/response-headers/).
        * An HTTP Status Code different than the default: [Response - Change Status Code](https://fastapi.tiangolo.com/advanced/response-change-status-code/).
    * All of this while still being able to return arbitrary objects (`dict`, DB model, etc).
    * Update attribution to Hug, for inspiring the `response` parameter pattern.
    * PR [#294](https://github.com/tiangolo/fastapi/pull/294).

## 0.28.0 (2019-06-05)

* Implement dependency cache per request.
    * This avoids calling each dependency multiple times for the same request.
    * This is useful while calling external services, performing costly computation, etc.
    * This also means that if a dependency was declared as a *path operation decorator* dependency, possibly at the router level (with `.include_router()`) and then it is declared again in a specific *path operation*, the dependency will be called only once.
    * The cache can be disabled per dependency declaration, using `use_cache=False` as in `Depends(your_dependency, use_cache=False)`.
    * Updated docs at: [Using the same dependency multiple times](https://fastapi.tiangolo.com/tutorial/dependencies/sub-dependencies/#using-the-same-dependency-multiple-times).
    * PR [#292](https://github.com/tiangolo/fastapi/pull/292).

* Implement dependency overrides for testing.
    * This allows using overrides/mocks of dependencies during tests.
    * New docs: [Testing Dependencies with Overrides](https://fastapi.tiangolo.com/advanced/testing-dependencies/).
    * PR [#291](https://github.com/tiangolo/fastapi/pull/291).

## 0.27.2 (2019-06-03)

* Fix path and query parameters receiving `dict` as a valid type. It should be mapped to a body payload. PR [#287](https://github.com/tiangolo/fastapi/pull/287). Updated docs at: [Query parameter list / multiple values with defaults: Using `list`](https://fastapi.tiangolo.com/tutorial/query-params-str-validations/#using-list).

## 0.27.1 (2019-06-03)

* Fix `auto_error=False` handling in `HTTPBearer` security scheme. Do not `raise` when there's an incorrect `Authorization` header if `auto_error=False`. PR [#282](https://github.com/tiangolo/fastapi/pull/282).

* Fix type declaration of `HTTPException`. PR [#279](https://github.com/tiangolo/fastapi/pull/279).

## 0.27.0 (2019-05-30)

* Fix broken link in docs about OAuth 2.0 with scopes. PR [#275](https://github.com/tiangolo/fastapi/pull/275) by [@dmontagu](https://github.com/dmontagu).

* Refactor param extraction using Pydantic `Field`:
    * Large refactor, improvement, and simplification of param extraction from *path operations*.
    * Fix/add support for list *query parameters* with list defaults. New documentation: [Query parameter list / multiple values with defaults](https://fastapi.tiangolo.com/tutorial/query-params-str-validations/#query-parameter-list-multiple-values-with-defaults).
    * Add support for enumerations in *path operation* parameters. New documentation: [Path Parameters: Predefined values](https://fastapi.tiangolo.com/tutorial/path-params/#predefined-values).
    * Add support for type annotations using `Optional` as in `param: Optional[str] = None`. New documentation: [Optional type declarations](https://fastapi.tiangolo.com/tutorial/query-params/#optional-type-declarations).
    * PR [#278](https://github.com/tiangolo/fastapi/pull/278).

## 0.26.0 (2019-05-29)

* Separate error handling for validation errors.
    * This will allow developers to customize the exception handlers.
    * Document better how to handle exceptions and use error handlers.
    * Include `RequestValidationError` and `WebSocketRequestValidationError` (this last one will be useful once [encode/starlette#527](https://github.com/encode/starlette/pull/527) or equivalent is merged).
    * New documentation about exceptions handlers:
        * [Install custom exception handlers](https://fastapi.tiangolo.com/tutorial/handling-errors/#install-custom-exception-handlers).
        * [Override the default exception handlers](https://fastapi.tiangolo.com/tutorial/handling-errors/#override-the-default-exception-handlers).
        * [Reuse **FastAPI's** exception handlers](https://fastapi.tiangolo.com/tutorial/handling-errors/#reuse-fastapis-exception-handlers).
    * PR [#273](https://github.com/tiangolo/fastapi/pull/273).

* Fix support for *paths* in *path parameters* without needing explicit `Path(...)`.
    * PR [#256](https://github.com/tiangolo/fastapi/pull/256).
    * Documented in PR [#272](https://github.com/tiangolo/fastapi/pull/272) by [@wshayes](https://github.com/wshayes).
    * New documentation at: [Path Parameters containing paths](https://fastapi.tiangolo.com/tutorial/path-params/#path-parameters-containing-paths).

* Update docs for testing FastAPI. Include using `POST`, sending JSON, testing headers, etc. New documentation: [Testing](https://fastapi.tiangolo.com/tutorial/testing/#testing-extended-example). PR [#271](https://github.com/tiangolo/fastapi/pull/271).

* Fix type declaration of `response_model` to allow generic Python types as `List[Model]`. Mainly to fix `mypy` for users. PR [#266](https://github.com/tiangolo/fastapi/pull/266).

## 0.25.0 (2019-05-27)

* Add support for Pydantic's `include`, `exclude`, `by_alias`.
    * Update documentation: [Response Model](https://fastapi.tiangolo.com/tutorial/response-model/#response_model_include-and-response_model_exclude).
    * Add docs for: [Body - updates](https://fastapi.tiangolo.com/tutorial/body-updates/), using Pydantic's `skip_defaults`.
    * Add method consistency tests.
    * PR [#264](https://github.com/tiangolo/fastapi/pull/264).

* Add `CONTRIBUTING.md` file to GitHub, to help new contributors. PR [#255](https://github.com/tiangolo/fastapi/pull/255) by [@wshayes](https://github.com/wshayes).

* Add support for Pydantic's `skip_defaults`:
    * There's a new *path operation decorator* parameter `response_model_skip_defaults`.
        * The name of the parameter will most probably change in a future version to `response_skip_defaults`, `model_skip_defaults` or something similar.
    * New [documentation section about using `response_model_skip_defaults`](https://fastapi.tiangolo.com/tutorial/response-model/#response-model-encoding-parameters).
    * PR [#248](https://github.com/tiangolo/fastapi/pull/248) by [@wshayes](https://github.com/wshayes).

## 0.24.0 (2019-05-24)

* Add support for WebSockets with dependencies and parameters.
    * Support included for:
        * `Depends`
        * `Security`
        * `Cookie`
        * `Header`
        * `Path`
        * `Query`
        * ...as these are compatible with the WebSockets protocol (e.g. `Body` is not).
    * [Updated documentation for WebSockets](https://fastapi.tiangolo.com/advanced/websockets/).
    * PR [#178](https://github.com/tiangolo/fastapi/pull/178) by [@jekirl](https://github.com/jekirl).

* Upgrade the compatible version of Pydantic to `0.26.0`.
    * This includes JSON Schema support for IP address and network objects, bug fixes, and other features.
    * PR [#247](https://github.com/tiangolo/fastapi/pull/247) by [@euri10](https://github.com/euri10).

## 0.23.0 (2019-05-21)

* Upgrade the compatible version of Starlette to `0.12.0`.
    * This includes support for ASGI 3 (the latest version of the standard).
    * It's now possible to use [Starlette's `StreamingResponse`](https://www.starlette.dev/responses/#streamingresponse) with iterators, like [file-like](https://docs.python.org/3/glossary.html#term-file-like-object) objects (as those returned by `open()`).
    * It's now possible to use the low level utility `iterate_in_threadpool` from `starlette.concurrency` (for advanced scenarios).
    * PR [#243](https://github.com/tiangolo/fastapi/pull/243).

* Add OAuth2 redirect page for Swagger UI. This allows having delegated authentication in the Swagger UI docs. For this to work, you need to add `{your_origin}/docs/oauth2-redirect` to the allowed callbacks in your OAuth2 provider (in Auth0, Facebook, Google, etc).
    * For example, during development, it could be `http://localhost:8000/docs/oauth2-redirect`.
    * Keep in mind that this callback URL is independent of whichever one is used by your frontend. You might also have another callback at `https://yourdomain.com/login/callback`.
    * This is only to allow delegated authentication in the API docs with Swagger UI.
    * PR [#198](https://github.com/tiangolo/fastapi/pull/198) by [@steinitzu](https://github.com/steinitzu).

* Make Swagger UI and ReDoc route handlers (*path operations*) be `async` functions instead of lambdas to improve performance. PR [#241](https://github.com/tiangolo/fastapi/pull/241) by [@Trim21](https://github.com/Trim21).

* Make Swagger UI and ReDoc URLs parameterizable, allowing to host and serve local versions of them and have offline docs. PR [#112](https://github.com/tiangolo/fastapi/pull/112) by [@euri10](https://github.com/euri10).

## 0.22.0 (2019-05-16)

* Add support for `dependencies` parameter:
    * A parameter in *path operation decorators*, for dependencies that should be executed but the return value is not important or not used in the *path operation function*.
    * A parameter in the `.include_router()` method of FastAPI applications and routers, to include dependencies that should be executed in each *path operation* in a router.
        * This is useful, for example, to require authentication or permissions in specific group of *path operations*.
        * Different `dependencies` can be applied to different routers.
    * These `dependencies` are run before the normal parameter dependencies. And normal dependencies are run too. They can be combined.
    * Dependencies declared in a router are executed first, then the ones defined in *path operation decorators*, and then the ones declared in normal parameters. They are all combined and executed.
    * All this also supports using `Security` with `scopes` in those `dependencies` parameters, for more advanced OAuth 2.0 security scenarios with scopes.
    * New documentation about [dependencies in *path operation decorators*](https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-in-path-operation-decorators/).
    * New documentation about [dependencies in the `include_router()` method](https://fastapi.tiangolo.com/tutorial/bigger-applications/#include-an-apirouter-with-a-prefix-tags-responses-and-dependencies).
    * PR [#235](https://github.com/tiangolo/fastapi/pull/235).

* Fix OpenAPI documentation of Starlette URL convertors. Specially useful when using `path` convertors, to take a whole path as a parameter, like `/some/url/{p:path}`. PR [#234](https://github.com/tiangolo/fastapi/pull/234) by [@euri10](https://github.com/euri10).

* Make default parameter utilities exported from `fastapi` be functions instead of classes (the new functions return instances of those classes). To be able to override the return types and fix `mypy` errors in FastAPI's users' code. Applies to `Path`, `Query`, `Header`, `Cookie`, `Body`, `Form`, `File`, `Depends`, and `Security`. PR [#226](https://github.com/tiangolo/fastapi/pull/226) and PR [#231](https://github.com/tiangolo/fastapi/pull/231).

* Separate development scripts `test.sh`, `lint.sh`, and `format.sh`. PR [#232](https://github.com/tiangolo/fastapi/pull/232).

* Re-enable `black` formatting checks for Python 3.7. PR [#229](https://github.com/tiangolo/fastapi/pull/229) by [@zamiramir](https://github.com/zamiramir).

## 0.21.0 (2019-05-15)

* On body parsing errors, raise `from` previous exception, to allow better introspection in logging code. PR [#192](https://github.com/tiangolo/fastapi/pull/195) by [@ricardomomm](https://github.com/ricardomomm).

* Use Python logger named "`fastapi`" instead of root logger. PR [#222](https://github.com/tiangolo/fastapi/pull/222) by [@euri10](https://github.com/euri10).

* Upgrade Pydantic to version 0.25. PR [#225](https://github.com/tiangolo/fastapi/pull/225) by [@euri10](https://github.com/euri10).

* Fix typo in routing. PR [#221](https://github.com/tiangolo/fastapi/pull/221) by [@djlambert](https://github.com/djlambert).

## 0.20.1 (2019-05-11)

* Add typing information to package including file `py.typed`. PR [#209](https://github.com/tiangolo/fastapi/pull/209) by [@meadsteve](https://github.com/meadsteve).

* Add FastAPI bot for Gitter. To automatically announce new releases. PR [#189](https://github.com/tiangolo/fastapi/pull/189).

## 0.20.0 (2019-04-27)

* Upgrade OAuth2:
    * Upgrade Password flow using Bearer tokens to use the correct HTTP status code 401 `UNAUTHORIZED`, with `WWW-Authenticate` headers.
    * Update, simplify, and improve all the [security docs](https://fastapi.tiangolo.com/advanced/security/).
    * Add new `scope_str` to `SecurityScopes` and update docs: [OAuth2 scopes](https://fastapi.tiangolo.com/advanced/security/oauth2-scopes/).
    * Update docs, images, tests.
    * PR [#188](https://github.com/tiangolo/fastapi/pull/188).

* Include [Hypercorn](https://gitlab.com/pgjones/hypercorn) as an alternative ASGI server in the docs. PR [#187](https://github.com/tiangolo/fastapi/pull/187).

* Add docs for [Static Files](https://fastapi.tiangolo.com/tutorial/static-files/) and [Templates](https://fastapi.tiangolo.com/advanced/templates/). PR [#186](https://github.com/tiangolo/fastapi/pull/186).

* Add docs for handling [Response Cookies](https://fastapi.tiangolo.com/advanced/response-cookies/) and [Response Headers](https://fastapi.tiangolo.com/advanced/response-headers/). PR [#185](https://github.com/tiangolo/fastapi/pull/185).

* Fix typos in docs. PR [#176](https://github.com/tiangolo/fastapi/pull/176) by [@chdsbd](https://github.com/chdsbd).

## 0.19.0 (2019-04-26)

* Rename *path operation decorator* parameter `content_type` to `response_class`. PR [#183](https://github.com/tiangolo/fastapi/pull/183).

* Add docs:
    * How to use the `jsonable_encoder` in [JSON compatible encoder](https://fastapi.tiangolo.com/tutorial/encoder/).
    * How to [Return a Response directly](https://fastapi.tiangolo.com/advanced/response-directly/).
    * Update how to use a [Custom Response Class](https://fastapi.tiangolo.com/advanced/custom-response/).
    * PR [#184](https://github.com/tiangolo/fastapi/pull/184).

## 0.18.0 (2019-04-22)

* Add docs for [HTTP Basic Auth](https://fastapi.tiangolo.com/advanced/custom-response/). PR [#177](https://github.com/tiangolo/fastapi/pull/177).

* Upgrade HTTP Basic Auth handling with automatic headers (automatic browser login prompt). PR [#175](https://github.com/tiangolo/fastapi/pull/175).

* Update dependencies for security. PR [#174](https://github.com/tiangolo/fastapi/pull/174).

* Add docs for [Middleware](https://fastapi.tiangolo.com/tutorial/middleware/). PR [#173](https://github.com/tiangolo/fastapi/pull/173).

## 0.17.0 (2019-04-20)

* Make Flit publish from CI. PR [#170](https://github.com/tiangolo/fastapi/pull/170).

* Add documentation about handling [CORS (Cross-Origin Resource Sharing)](https://fastapi.tiangolo.com/tutorial/cors/). PR [#169](https://github.com/tiangolo/fastapi/pull/169).

* By default, encode by alias. This allows using Pydantic `alias` parameters working by default. PR [#168](https://github.com/tiangolo/fastapi/pull/168).

## 0.16.0 (2019-04-16)

* Upgrade *path operation* `docstring` parsing to support proper Markdown descriptions. New documentation at [Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/#description-from-docstring). PR [#163](https://github.com/tiangolo/fastapi/pull/163).

* Refactor internal usage of Pydantic to use correct data types. PR [#164](https://github.com/tiangolo/fastapi/pull/164).

* Upgrade Pydantic to version `0.23`. PR [#160](https://github.com/tiangolo/fastapi/pull/160) by [@euri10](https://github.com/euri10).

* Fix typo in Tutorial about Extra Models. PR [#159](https://github.com/tiangolo/fastapi/pull/159) by [@danielmichaels](https://github.com/danielmichaels).

* Fix [Query Parameters](https://fastapi.tiangolo.com/tutorial/query-params/) URL examples in docs. PR [#157](https://github.com/tiangolo/fastapi/pull/157) by [@hayata-yamamoto](https://github.com/hayata-yamamoto).

## 0.15.0 (2019-04-14)

* Add support for multiple file uploads (as a single form field). New docs at: [Multiple file uploads](https://fastapi.tiangolo.com/tutorial/request-files/#multiple-file-uploads). PR [#158](https://github.com/tiangolo/fastapi/pull/158).

* Add docs for: [Additional Status Codes](https://fastapi.tiangolo.com/advanced/additional-status-codes/). PR [#156](https://github.com/tiangolo/fastapi/pull/156).

## 0.14.0 (2019-04-12)

* Improve automatically generated names of *path operations* in OpenAPI (in API docs). A function `read_items` instead of having a generated name "Read Items Get" will have "Read Items". PR [#155](https://github.com/tiangolo/fastapi/pull/155).

* Add docs for: [Testing **FastAPI**](https://fastapi.tiangolo.com/tutorial/testing/). PR [#151](https://github.com/tiangolo/fastapi/pull/151).

* Update `/docs` Swagger UI to enable deep linking. This allows sharing the URL pointing directly to the *path operation* documentation in the docs. PR [#148](https://github.com/tiangolo/fastapi/pull/148) by [@wshayes](https://github.com/wshayes).

* Update development dependencies, `Pipfile.lock`. PR [#150](https://github.com/tiangolo/fastapi/pull/150).

* Include Falcon and Hug in: [Alternatives, Inspiration and Comparisons](https://fastapi.tiangolo.com/alternatives/).

## 0.13.0 (2019-04-09)

* Improve/upgrade OAuth2 scopes support with `SecurityScopes`:
    * `SecurityScopes` can be declared as a parameter like `Request`, to get the scopes of all super-dependencies/dependants.
    * Improve `Security` handling, merging scopes when declaring `SecurityScopes`.
    * Allow using `SecurityBase` (like `OAuth2`) classes with `Depends` and still document them. `Security` now is needed only to declare `scopes`.
    * Updated docs about: [OAuth2 with Password (and hashing), Bearer with JWT tokens](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/).
    * New docs about: [OAuth2 scopes](https://fastapi.tiangolo.com/advanced/security/oauth2-scopes/).
    * PR [#141](https://github.com/tiangolo/fastapi/pull/141).

## 0.12.1 (2019-04-05)

* Fix bug: handling additional `responses` in `APIRouter.include_router()`. PR [#140](https://github.com/tiangolo/fastapi/pull/140).

* Fix typo in SQL tutorial. PR [#138](https://github.com/tiangolo/fastapi/pull/138) by [@mostaphaRoudsari](https://github.com/mostaphaRoudsari).

* Fix typos in section about nested models and OAuth2 with JWT. PR [#127](https://github.com/tiangolo/fastapi/pull/127) by [@mmcloud](https://github.com/mmcloud).

## 0.12.0 (2019-04-05)

* Add additional `responses` parameter to *path operation decorators* to extend responses in OpenAPI (and API docs).
    * It also allows extending existing responses generated from `response_model`, declare other media types (like images), etc.
    * The new documentation is here: [Additional Responses](https://fastapi.tiangolo.com/advanced/additional-responses/).
    * `responses` can also be added to `.include_router()`, the updated docs are here: [Bigger Applications](https://fastapi.tiangolo.com/tutorial/bigger-applications/#add-some-custom-tags-and-responses).
    * PR [#97](https://github.com/tiangolo/fastapi/pull/97) originally initiated by [@barsi](https://github.com/barsi).
* Update `scripts/test-cov-html.sh` to allow passing extra parameters like `-vv`, for development.

## 0.11.0 (2019-04-03)

* Add `auto_error` parameter to security utility functions. Allowing them to be optional. Also allowing to have multiple alternative security schemes that are then checked in a single dependency instead of each one verifying and returning the error to the client automatically when not satisfied. PR [#134](https://github.com/tiangolo/fastapi/pull/134).

* Update [SQL Tutorial](https://fastapi.tiangolo.com/tutorial/sql-databases/#create-a-middleware-to-handle-sessions) to close database sessions even when there are exceptions. PR [#89](https://github.com/tiangolo/fastapi/pull/89) by [@alexiri](https://github.com/alexiri).

* Fix duplicate dependency in `pyproject.toml`. PR [#128](https://github.com/tiangolo/fastapi/pull/128) by [@zxalif](https://github.com/zxalif).

## 0.10.3 (2019-03-30)

* Add Gitter chat, badge, links, etc. [https://gitter.im/tiangolo/fastapi](https://gitter.im/tiangolo/fastapi) . PR [#117](https://github.com/tiangolo/fastapi/pull/117).

* Add docs about [Extending OpenAPI](https://fastapi.tiangolo.com/advanced/extending-openapi/). PR [#126](https://github.com/tiangolo/fastapi/pull/126).

* Make Travis run Ubuntu Xenial (newer version) and Python 3.7 instead of Python 3.7-dev. PR [#92](https://github.com/tiangolo/fastapi/pull/92) by [@blueyed](https://github.com/blueyed).

* Fix duplicated param variable creation. PR [#123](https://github.com/tiangolo/fastapi/pull/123) by [@yihuang](https://github.com/yihuang).

* Add note in [Response Model docs](https://fastapi.tiangolo.com/tutorial/response-model/) about why using a function parameter instead of a function return type annotation. PR [#109](https://github.com/tiangolo/fastapi/pull/109) by [@JHSaunders](https://github.com/JHSaunders).

* Fix event docs (startup/shutdown) function name. PR [#105](https://github.com/tiangolo/fastapi/pull/105) by [@stratosgear](https://github.com/stratosgear).

## 0.10.2 (2019-03-29)

* Fix OpenAPI (JSON Schema) for declarations of Python `Union` (JSON Schema `additionalProperties`). PR [#121](https://github.com/tiangolo/fastapi/pull/121).

* Update [Background Tasks](https://fastapi.tiangolo.com/tutorial/background-tasks/) with a note on Celery.

* Document response models using unions and lists, updated at: [Extra Models](https://fastapi.tiangolo.com/tutorial/extra-models/). PR [#108](https://github.com/tiangolo/fastapi/pull/108).

## 0.10.1 (2019-03-25)

* Add docs and tests for [encode/databases](https://github.com/encode/databases). New docs at: [Async SQL (Relational) Databases](https://fastapi.tiangolo.com/advanced/async-sql-databases/). PR [#107](https://github.com/tiangolo/fastapi/pull/107).

## 0.10.0 (2019-03-24)

* Add support for Background Tasks in *path operation functions* and dependencies. New documentation about [Background Tasks is here](https://fastapi.tiangolo.com/tutorial/background-tasks/). PR [#103](https://github.com/tiangolo/fastapi/pull/103).

* Add support for `.websocket_route()` in `APIRouter`. PR [#100](https://github.com/tiangolo/fastapi/pull/100) by [@euri10](https://github.com/euri10).

* New docs section about [Events: startup - shutdown](https://fastapi.tiangolo.com/advanced/events/). PR [#99](https://github.com/tiangolo/fastapi/pull/99).

## 0.9.1 (2019-03-22)

* Document receiving [Multiple values with the same query parameter](https://fastapi.tiangolo.com/tutorial/query-params-str-validations/#query-parameter-list-multiple-values) and [Duplicate headers](https://fastapi.tiangolo.com/tutorial/header-params/#duplicate-headers). PR [#95](https://github.com/tiangolo/fastapi/pull/95).

## 0.9.0 (2019-03-22)

* Upgrade compatible Pydantic version to `0.21.0`. PR [#90](https://github.com/tiangolo/fastapi/pull/90).

* Add documentation for: [Application Configuration](https://fastapi.tiangolo.com/tutorial/application-configuration/).

* Fix typo in docs. PR [#76](https://github.com/tiangolo/fastapi/pull/76) by [@matthewhegarty](https://github.com/matthewhegarty).

* Fix link in "Deployment" to "Bigger Applications".

## 0.8.0 (2019-03-16)

* Make development scripts executable. PR [#76](https://github.com/tiangolo/fastapi/pull/76) by [@euri10](https://github.com/euri10).

* Add support for adding `tags` in `app.include_router()`. PR [#55](https://github.com/tiangolo/fastapi/pull/55) by [@euri10](https://github.com/euri10). Documentation updated in the section: [Bigger Applications](https://fastapi.tiangolo.com/tutorial/bigger-applications/).

* Update docs related to Uvicorn to use new `--reload` option from version `0.5.x`. PR [#74](https://github.com/tiangolo/fastapi/pull/74).

* Update `isort` imports and scripts to be compatible with newer versions. PR [#75](https://github.com/tiangolo/fastapi/pull/75).

## 0.7.1 (2019-03-04)

* Update [technical details about `async def` handling](https://fastapi.tiangolo.com/async/#path-operation-functions) with respect to previous frameworks. PR [#64](https://github.com/tiangolo/fastapi/pull/64) by [@haizaar](https://github.com/haizaar).

* Add [deployment documentation for Docker in Raspberry Pi](https://fastapi.tiangolo.com/deployment/#raspberry-pi-and-other-architectures) and other architectures.

* Trigger Docker images build on Travis CI automatically. PR [#65](https://github.com/tiangolo/fastapi/pull/65).

## 0.7.0 (2019-03-03)

* Add support for `UploadFile` in `File` parameter annotations.
    * This includes a file-like interface.
    * Here's the updated documentation for declaring [`File` parameters with `UploadFile`](https://fastapi.tiangolo.com/tutorial/request-files/#file-parameters-with-uploadfile).
    * And here's the updated documentation for using [`Form` parameters mixed with `File` parameters, supporting `bytes` and `UploadFile`](https://fastapi.tiangolo.com/tutorial/request-forms-and-files/) at the same time.
    * PR [#63](https://github.com/tiangolo/fastapi/pull/63).

## 0.6.4 (2019-03-02)

* Add [technical details about `async def` handling to docs](https://fastapi.tiangolo.com/async/#very-technical-details). PR [#61](https://github.com/tiangolo/fastapi/pull/61).

* Add docs for [Debugging FastAPI applications in editors](https://fastapi.tiangolo.com/tutorial/debugging/).

* Clarify [Bigger Applications deployed with Docker](https://fastapi.tiangolo.com/deployment/#bigger-applications).

* Fix typos in docs.

* Add section about [History, Design and Future](https://fastapi.tiangolo.com/history-design-future/).

* Add docs for using [WebSockets with **FastAPI**](https://fastapi.tiangolo.com/advanced/websockets/). PR [#62](https://github.com/tiangolo/fastapi/pull/62).

## 0.6.3 (2019-02-23)

* Add Favicons to docs. PR [#53](https://github.com/tiangolo/fastapi/pull/53).

## 0.6.2 (2019-02-23)

* Introduce new project generator based on FastAPI and PostgreSQL: [https://github.com/tiangolo/full-stack-fastapi-postgresql](https://github.com/tiangolo/full-stack-fastapi-postgresql). PR [#52](https://github.com/tiangolo/fastapi/pull/52).

* Update [SQL tutorial with SQLAlchemy, using `Depends` to improve editor support and reduce code repetition](https://fastapi.tiangolo.com/tutorial/sql-databases/). PR [#52](https://github.com/tiangolo/fastapi/pull/52).

* Improve middleware naming in tutorial for SQL with SQLAlchemy [https://fastapi.tiangolo.com/tutorial/sql-databases/](https://fastapi.tiangolo.com/tutorial/sql-databases/).

## 0.6.1 (2019-02-20)

* Add docs for GraphQL: [https://fastapi.tiangolo.com/advanced/graphql/](https://fastapi.tiangolo.com/advanced/graphql/). PR [#48](https://github.com/tiangolo/fastapi/pull/48).

## 0.6.0 (2019-02-19)

* Update SQL with SQLAlchemy tutorial at [https://fastapi.tiangolo.com/tutorial/sql-databases/](https://fastapi.tiangolo.com/tutorial/sql-databases/) using the new official `request.state`. PR [#45](https://github.com/tiangolo/fastapi/pull/45).

* Upgrade Starlette to version `0.11.1` and add required compatibility changes. PR [#44](https://github.com/tiangolo/fastapi/pull/44).

## 0.5.1 (2019-02-18)

* Add section about [helping and getting help with **FastAPI**](https://fastapi.tiangolo.com/help-fastapi/).

* Add note about [path operations order in docs](https://fastapi.tiangolo.com/tutorial/path-params/#order-matters).

* Update [section about error handling](https://fastapi.tiangolo.com/tutorial/handling-errors/) with more information and make relation with Starlette error handling utilities more explicit. PR [#41](https://github.com/tiangolo/fastapi/pull/41).

* Add [Development - Contributing section to the docs](). PR [#42](https://github.com/tiangolo/fastapi/pull/42).

## 0.5.0 (2019-02-16)

* Add new `HTTPException` with support for custom headers. With new documentation for handling errors at: [https://fastapi.tiangolo.com/tutorial/handling-errors/](https://fastapi.tiangolo.com/tutorial/handling-errors/). PR [#35](https://github.com/tiangolo/fastapi/pull/35).

* Add [documentation to use Starlette `Request` object](https://fastapi.tiangolo.com/advanced/using-request-directly/) directly. Check [#25](https://github.com/tiangolo/fastapi/pull/25) by [@euri10](https://github.com/euri10).

* Add issue templates to simplify reporting bugs, getting help, etc: [#34](https://github.com/tiangolo/fastapi/pull/34).

* Update example for the SQLAlchemy tutorial at [https://fastapi.tiangolo.com/tutorial/sql-databases/](https://fastapi.tiangolo.com/tutorial/sql-databases/) using middleware and database session attached to request.

## 0.4.0 (2019-02-16)

* Add `openapi_prefix`, support for reverse proxy and mounting sub-applications. See the docs at [https://fastapi.tiangolo.com/advanced/sub-applications-proxy/](https://fastapi.tiangolo.com/advanced/sub-applications-proxy/): [#26](https://github.com/tiangolo/fastapi/pull/26) by [@kabirkhan](https://github.com/kabirkhan).

* Update [docs/tutorial for SQLAlchemy](https://fastapi.tiangolo.com/tutorial/sql-databases/) including note about _DB Browser for SQLite_.

## 0.3.0 (2019-02-12)

* Fix/add SQLAlchemy support, including ORM, and update [docs for SQLAlchemy](https://fastapi.tiangolo.com/tutorial/sql-databases/): [#30](https://github.com/tiangolo/fastapi/pull/30).

## 0.2.1 (2019-02-12)

* Fix `jsonable_encoder` for Pydantic models with `Config` but without `json_encoders`: [#29](https://github.com/tiangolo/fastapi/pull/29).

## 0.2.0 (2019-02-08)

* Fix typos in Security section: [#24](https://github.com/tiangolo/fastapi/pull/24) by [@kkinder](https://github.com/kkinder).

* Add support for Pydantic custom JSON encoders: [#21](https://github.com/tiangolo/fastapi/pull/21) by [@euri10](https://github.com/euri10).

## 0.1.19 (2019-02-01)

* Upgrade Starlette version to the current latest `0.10.1`: [#17](https://github.com/tiangolo/fastapi/pull/17) by [@euri10](https://github.com/euri10).