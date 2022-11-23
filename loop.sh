set -e 
touch floating_paths.txt
touch floating_samples_clades.txt
for f in *pb.gz ; do 
    export PREFIX=${f%.all.masked.pb.gz} ; 
    matUtils annotate -T 4 -i $PREFIX.all.masked.pb.gz -P floating_paths.txt floating_samples_clades.txt -o $PREFIX.pb ; 
    gzip $PREFIX.pb ; 
    cd automate-lineages-prototype ;
    snakemake -c1 -s flag_lineages.smk ../$PREFIX.proposed.report.tsv ; 
    cd .. ; 
    matUtils extract -i $PREFIX.proposed.pb -C floating_paths.base.txt ; 
    awk -F'\t' '{{print $1"\t"$3}}' floating_paths.base.txt | tail -n +2 > floating_paths.txt ; 
    python3 extract_sample_clades.py $PREFIX.proposed.pb > floating_samples_clades.txt ; 
done
