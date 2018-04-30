#bin/bash
for a in {R..R};do
for b in {A..Z};do
for c in {A..Z};do
for d in {A..Z};do
for e in {0..9};do
for f in {0..9};do
for h in {0..9};do
for j in {0..9};do
VAL="NCL-$a$b$c$d-$e$f$h$j"
md5=$(echo -n $VAL | md5sum)
echo $md5 $VAL >> md5.txt
sha1=$(echo -n $VAL | sha1sum)
echo $sha1 $VAL >> sha1.txt
sha256=$(echo -n $VAL | sha256sum)
echo $sha256 $VAL >> sha256.txt
echo $VAL
done
done
done
done
done
done
done
done
echo "Done"
