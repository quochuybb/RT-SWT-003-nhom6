## 0.92.0 (2023-02-14)

🚨 This is a security fix. Please upgrade as soon as possible.

### Upgrades

* ⬆️ Upgrade Starlette to 0.25.0. PR [#5996](https://github.com/tiangolo/fastapi/pull/5996) by [@tiangolo](https://github.com/tiangolo).
    * This solves a vulnerability that could allow denial of service attacks by using many small multipart fields/files (parts), consuming high CPU and memory.
    * Only applications **not using forms** (e.g. file uploads) could be affected.
    * For most cases, upgrading won't have any breaking changes.