// Tesseract class to output text and score
// Chris G. Willcocks

#include <fstream>
#include <tesseract/baseapi.h>
#include <leptonica/allheaders.h>

int main(int argc,char *argv[])
{
	char *outText;

	tesseract::TessBaseAPI *api = new tesseract::TessBaseAPI();

    	// Initialize tesseract-ocr with English, without specifying tessdata path
    	if (api->Init(NULL, NULL, tesseract::OEM_DEFAULT)) {
        	fprintf(stderr, "Could not initialize tesseract.\n");
       		exit(1);
    	}

	// Setup data
 	api->SetPageSegMode(tesseract::PSM_AUTO);

	// Open input image with leptonica library
	Pix *image = pixRead(argv[2]);
	api->SetImage(image);

	// Get OCR result
	outText = api->GetUTF8Text();

	// printf("OCR output:\n%s", outText);
	// printf("Score:%d\n", api->MeanTextConf());
	// printf("Directory of output: %s\n", argv[2]);	
	// std::string version = tesseract::TessBaseAPI::Version();
	// printf("Version: %s\n",version.c_str());
	printf(".");

	std::ofstream fs;
	std::string s = argv[3];
		    s = s+".txt";
	fs.open(s.c_str(), std::ios::out|std::ios::binary);
	fs << api->MeanTextConf();
	fs << "\n";
	fs << outText;
	fs.close();

	// Destroy used object and release memory
	api->End();
	delete [] outText;
	pixDestroy(&image);

	return 0;
}
