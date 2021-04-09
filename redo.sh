echo "make avhymns"
mkdir avhymns
cp avhymns.css avhymns/
mkdir avhymns/fonts
cp fonts/siddhanta.ttf avhymns/fonts/
python make_hymns_01.py AVS2.html avhymns
