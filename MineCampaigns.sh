node getthemposts.js $1
rm output/*
python createCSVData.py
echo "Job's done."