# timeseries-lineage-analysis
Repository containing scripts and data for the analysis of the persistence and growth of arbitrary lineage annotations for SARS-CoV-2 over a series of public phylogenies. 

## Usage

You can obtain a historical time series of protobufs by choosing dates and downloading those days' global phylogenies from [here](http://hgdownload.soe.ucsc.edu/goldenPath/wuhCor1/UShER_SARS-CoV-2/). 

You will need [BTE](https://github.com/jmcbroome/BTE) and [matUtils](https://github.com/yatisht/usher) to be available in your environment. You can install them locally from their repositories or through the bioconda channel.

This repository uses github submodules to wrap the automated lineage prototype. When you clone it, you will need to use --recurse-submodules to correctly initialize it.

```
conda create -n timelin -c conda-forge -c bioconda usher bte pandas snakemake
conda activate timelin
git clone --recurse-submodules https://github.com/jmcbroome/lineage-analysis
```

Once your environment is set up and your files are available, run the following:

```
bash ./loop.sh
```

This automatically infers new lineages on each tree in your time series, propagating inferred lineages between trees. Note that the glob order is alphanumeric- if you use the standard tree name formatting (e.g. public-YYYY-MM-DD) then it should be in the correct time order as well.

Once you've generated all your results files, collect some statistics by running the following.

```
for f in *proposed.pb ; do
    matUtils summary -i $f -c ${f%.proposed.pb}.cladestats.txt ;
done
```

```
python3 compile_reports.py -a
```

Your results will be visible in compiled_report.tsv. There are adjustable parameters for compile_reports.py (use --help).
