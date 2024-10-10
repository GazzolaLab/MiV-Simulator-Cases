# MiV Simulator Case Studies

### References

- Gfluct3
  * Destexhe, A et al. “Fluctuating synaptic conductances recreate in vivo-like activity in neocortical neurons.” Neuroscience vol. 107,1 (2001): 13-24. doi:10.1016/s0306-4522(01)00344-x


<details>

<summary>How to install?</summary>

### Suggested setup

1. Install [uv](https://docs.astral.sh/uv/)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Update `uv` environment variables

```bash
# SSL certificate for Python OpenSSL
export SSL_CERT_FILE=/etc/pki/tls/cert.pem
export REQUESTS_CA_BUNDLE=/etc/pki/tls/cert.pem

# UV cache directories
export UV_TOOL_DIR=$SCRATCH/uv/tools
export UV_TOOL_BIN_DIR=$SCRATCH/uv/bin
export UV_PYTHON_INSTALL_DIR=$SCRATCH/uv/python
export UV_CACHE_DIR=$SCRATCH/uv/cache
```

3. Load MPI and HDF5 modules, e.g.

```bash
module load gcc/13.2.0 phdf5/1.14.3 impi/21.9.0
module save default
```

4. Sync the project

Clone repository into $SCRATCH, `cd` into it, and run `uv sync`.
This will create a virtualenv in `.venv` that you can use

5. If using [neuroh5](https://github.com/iraikov/neuroh5), clone into $SCRATCH and build

```sh
git clone https://github.com/iraikov/neuroh5.git
cd neuroh5
cmake .
make 
```

Then add the build binaries to PATH:

```sh
export PATH=$SCRATCH/neuroh5/bin:$PATH
```

</details>