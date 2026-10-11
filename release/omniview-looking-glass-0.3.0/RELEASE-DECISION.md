# OmniView0.3.0 maintenance release decision

Accepted baseline: complete0.3.0 customer archive, SHA256 e669a17f0bd0ef1465f17f508d66a98c6a2d666ec1dd8aa559abaf4c23f8b14a.

Complete customer-visible delta: a pinned edited view restores as an unsaved draft when its full contents differ from the authoritative saved record; swapping and pin controls retain meaningful keyboard focus. Recognizable camera artwork now binds Windows shortcut/folder setup, the macOS application bundle and browser favicon. Windows shortcut persistence preserves Unicode extraction paths. The current assembler builds from maintained source rather than a private old candidate, excludes local shortcut/folder artifacts and preserves macOS executable mode. Guides match the actual launchers and current tested scope.

Decision: edit, restored_behavior/presentation, retain0.3.0. The accepted0.3.0 promise already includes preserving saved/draft state, comparison, portable Windows/macOS camera launch and the direct-versus-agent rendering workflow. This repair restores that promise and its requested native presentation; it adds no provider route, scene capability, data schema or new image workflow. The original direct-render capability addition from0.2.0 remains the reason for0.3.0; no fresh public release or announcement is inferred.
