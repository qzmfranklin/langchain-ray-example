
## Create `docs.ray.io`

```bash
tar xvJf archive.tar.xz
```

## Download `docs.ray.io`

```bash
wget -e robots=off --recursive --no-clobber --page-requisites --html-extension \
    --convert-links --restrict-file-names=windows \
    --domains docs.ray.io --no-parent https://docs.ray.io/en/master/
```

This command takes ~2 hours to complete in China. Not sure how quickly or slowly
it would be in the US.