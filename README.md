# Search Engine with LangChain + Ray

Reproducing https://www.anyscale.com/blog/llm-open-source-search-engine-langchain-ray.

## Step 1: Set up Ray cluster

- Install [kubectl](https://kubernetes.io/docs/tasks/tools/#kubectl).

- Install [helm](https://helm.sh/docs/intro/install/).

- Get access to a Kubernetes cluster.  Make sure the `kubectl` command works.

    ```bash
    kubectl get all
    ```

- Install the KubeRay operator.

    ```bash
    helm repo add kuberay https://ray-project.github.io/kuberay-helm/
    helm install kuberay-operator kuberay/kuberay-operator --version 0.5.0
    ```

- Install Ray cluster with the KubeRay operator.

    ```bash
    helm install raycluster kuberay/ray-cluster --version 0.5.0
    ```

    Wait for pods to start:

    ```bash
    watch -n 1 kubectl get pod
    ```

    Also, the kuberay-head-svc should be available:

    ```bash
    kubectl get service raycluster-kuberay-head-svc
    ```

- Forward Ray dashboard to local port 8265.

    ```bash
    kubectl port-forward --address 0.0.0.0 service/raycluster-kuberay-head-svc 8265:8265
    ```

    Open http://localhost:8265/ in a browser.

## Step 2: Build index

- Follow through [this README](data/README.md) to create sample data.

- Install Python3 dependencies.

    ```bash
    pip3 install -r requirements.txt
    ```

You may either build the index locally or with Ray.

A successful run would populate the `data/.faiss_index` directory. For example:

```text
[4.0K]  data/.faiss_index
├── [146M]  index.faiss
└── [ 17M]  index.pkl
```

### Build the index locally

```bash
build_index.py
```

> TIP: It's OK to run this script from any directory. It relocates to the
correct directory prior to execution.

### Build the index with Ray

**WARNING**: I have not successfully run this script.  It hangs at uploading the
local working directory to the Ray cluster.  It is possibly due to uploading to
gcs.

```bash
submit_build_index.py
```

> TIP: It's OK to run this script from any directory. It relocates to the
correct directory prior to execution.

## Step 3: Start server

```bash
./serve.py
```
