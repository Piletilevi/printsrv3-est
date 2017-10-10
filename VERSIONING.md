# Versioning and release management

Semantic versioning is required.

Code is released as tags prefixed by major and minor i.e. `0.2-lt-maxima`.  
Tag could be moved to different commit as needed.

When printsrv looks for update, it retrieves commit SHA from given tag name.  
Then update procedure reads version number from package.json at this SHA.  

Now versions from local and remote packaga.json are compared and if they differ,
update starts to fetch files.

Package file has section "updateFiles" i.e.
```
    "updateFiles": [{
        "repository": "printsrv",
        "sha": "488d013",
        "files": [
            { "remote": "dist/printsrv.exe", "local": "printsrv.exe" },
            { "remote": "ˇversion.py", "local": "printsrv/version.py" }
        ]
    }, {
        "repository": "printsrv",
        "sha": "1563c81",
        "files": [
            { "remote": "dist/w9xpopen.exe", "local": "w9xpopen.exe" }
        ]
    }, {
        "repository": "RasoASM",
        "sha": "b89fad8",
        "files": [
            { "remote": "update.py", "local": false },
            { "remote": "fiscal_lt.bat", "local": "fiscal_lt.bat" },
            { "remote": "fiscal_lt.ipy", "local": "fiscal_lt.ipy" },
            { "remote": "fiscal.py", "local": "fiscal.py" },
            { "remote": "package.json", "local": "package.json" },
            { "remote": "fiscal_lt.bat", "local": "fiscal_lt.bat" }
        ]
    }]
```

**Note**: package.json should not be included in "updateFiles.printsrv.files" lists. It gets
downloaded and saved as a last thing when all other files are already updated.


## To create a new release

1. Commit all changes for new release
2. Increment version number in package.json
3. Also update dependencies in package.json
3. Commit version increment with message `Release major.minor.patch`
4. Create a release (copy content from previous one and update where relevant)
5. Update and commit README.md to refer to new release
