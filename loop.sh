set -e 
#reset.
mv *all.masked* temp
mv *metadata.tsv.gz temp
rm public*
mv temp/* .
rm floating_paths.txt
rm floating_samples_clades.txt
#proceed.   
touch floating_paths.txt
touch floating_samples_clades.txt
for f in *pb.gz ; do 
    export PREFIX=${f%.all.masked.pb.gz} ; 
    python3 strip_annotations.py $PREFIX.all.masked.pb.gz $PREFIX.cleaned.pb ;
    matUtils annotate -T 4 -i $PREFIX.cleaned.pb -P floating_paths.txt -c floating_samples_clades.txt -o $PREFIX.pb ; 
    gzip $PREFIX.pb ; 
    cd automate-lineages-prototype ;
    snakemake -c1 -s flag_lineages.smk ../$PREFIX.proposed.report.tsv ; 
    cd .. ; 
    matUtils extract -i $PREFIX.proposed.pb -C floating_paths.base.txt ; 
    awk -F'\t' '{{print $1"\t"$3}}' floating_paths.base.txt | tail -n +2 > floating_paths.txt ; 
    python3 extract_sample_clades.py $PREFIX.proposed.pb > floating_samples_clades.txt ; 
done
