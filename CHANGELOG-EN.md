# Changelog

## 1.0.0 — 2026-10-09

- Localizes single-item and bulk-removal confirmation tokens to match the displayed interface language.
- Localizes warnings, bulk-removal confirmations, prompts, and detail labels in all ten language options.

- Translates application analysis reasons in both the Python and PowerShell versions into all ten languages.

- Localizes the PowerShell menu, report headings, and statuses in all ten languages; corrects accents in prompts.

- Localizes analysis report headings, counts, and statuses in all ten supported languages.

- Updates the run instructions to point directly to the correct project entry point.

- Fixes backup list construction and aborts removal if the registry backup is incomplete.
- Logs removals only after confirmed deletion and shows session metadata in both PowerShell and Python versions.

- Detects potentially orphaned uninstall entries without deleting application files.
- Requires explicit confirmation and backs up registry data before removal.
- Stops the operation if any selected key cannot be backed up.
- Logs only completed removals under LocalAppData.
- Adds a session banner with version, date/time, and detected language.


- Corrects accents and cedilla in interface text and documentation, aligns session headers, and updates agent instructions.

- Usage, dependency, and required-file documentation was reviewed to match current project behavior.

