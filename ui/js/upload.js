

	
function doGenerate_SRGAN(evt) {

	/*var fileInput = document.getElementById('srganFileUpload').files;
	if (!fileInput.length) {
		return alert('Please choose a file to upload first')
	}
	var file = fileInput[0]
	var filename = file.name;
	
	var formData = new FormData()
	formData.append(filename, file)
	console.log(filename)
	*/
	$.ajax({
		async: true,
		crossDomain: true,
		method: 'POST',
		url: 'https://rr6wq5je98.execute-api.ap-south-1.amazonaws.com/dev/srgans',
		processData: false,
		contentType: false,
		mimeType: "multipart/form-data"
	})
	.done(function (response){
		console.log(response);
		//document.getElementById('vaeresult').textContent = response;
		$("#srganImageResultLow").attr('src', `data:image/png;base64,${JSON.parse(response)["low_res"]}`);
		$("#srganImageResultFake").attr('src', `data:image/png;base64,${JSON.parse(response)["highres_fake"]}`);
		$("#srganImageResultReal").attr('src', `data:image/png;base64,${JSON.parse(response)["highres_real"]}`);
	})
	.fail(function(){
		alert("There was an error while sending prediction request to Pose Estimation model.");
	});
};
function generateToken(){
	$.ajax({
		async: true,
		crossDomain: true,
		method: 'POST',
		url: 'https://db0cvsqkq1.execute-api.ap-south-1.amazonaws.com/dev/nst',
		data: formData,
		processData: false,
		contentType: false,
		mimeType: "multipart/form-data"
	})
	.done(function (response){
		console.log(response);
		//document.getElementById('vaeresult').textContent = response;
		$("#capstone_classification_token").attr('src', `${JSON.parse(response)["token"]}`);
	})
	.fail(function(){
		alert("There was an error while sending prediction request to Image Caption model.");
	});

}
function uploadAndTrainClassificationUsingResnet(){

	var fileInput = document.getElementById('capstoneImageTrainUpload').files;
	if (!fileInput.length) {
		return alert('Please choose an a compressed file to train the classification model.')
	}
	var file = fileInput[0]
	var filename = file.name;
	
	var formData = new FormData()
	formData.append(filename, file)
	console.log(filename)
	
	
	$.ajax({
		async: true,
		crossDomain: true,
		method: 'POST',
		url: 'https://db0cvsqkq1.execute-api.ap-south-1.amazonaws.com/dev/nst',
		data: formData,
		processData: false,
		contentType: false,
		mimeType: "multipart/form-data"
	})
	.done(function (response){
		console.log(response);
		//document.getElementById('vaeresult').textContent = response;
		$("#capstone_classification_token").attr('src', `${JSON.parse(response)["token"]}`);
	})
	.fail(function(){
		alert("There was an error while sending prediction request to Image Caption model.");
	});

}


function uploadAndTestClassificationUsingResnet(){

	var fileInput = document.getElementById('capstoneImageTrainUpload').files;
	if (!fileInput.length) {
		return alert('Please choose an a compressed file to train the classification model.')
	}
	var file = fileInput[0]
	var filename = file.name;
	
	var formData = new FormData()
	formData.append(filename, file)
	var user_token = document.getElementById('token').files;
	formData.append('token', user_token)
	
	console.log(filename)
	
	console.log(user_token)
	
	$.ajax({
		async: true,
		crossDomain: true,
		method: 'POST',
		url: 'https://db0cvsqkq1.execute-api.ap-south-1.amazonaws.com/dev/nst',
		data: formData,
		processData: false,
		contentType: false,
		mimeType: "multipart/form-data"
	})
	.done(function (response){
		console.log(response);
		//document.getElementById('vaeresult').textContent = response;
		$("#capstone_classification_token").attr('src', `${JSON.parse(response)["token"]}`);
	})
	.fail(function(){
		alert("There was an error while sending prediction request to Image Caption model.");
	});

}
function do_BERT_NLP(evt){

	var context = document.getElementById('id_nlp-context').value;
	if (!context.length) {
		return alert('Please provide context text and question to answer!')
	}
	
	var formData = new FormData()
	formData.append("body",context)
	console.log(context)

	$.ajax({
		async: true,
		crossDomain: true,
		method: 'POST',
		url: 'https://5q79zh7pz8.execute-api.ap-south-1.amazonaws.com/dev/ask',
		data: formData,
		processData: false,
		ContentType: 'application/json'
		//mimeType: "multipart/form-data"
	})
	.done(function (response){
		console.log(response);
		//document.getElementById('vaeresult').textContent = response;
		$("#nlp_bert_answer").attr('src', `${JSON.parse(response)["answer"]}`);
	})
	.fail(function(){
		alert("There was an error while sending  request to NLP BERT model.");
	});


};


function handleFileSelectResnet(evt) {
	var files = evt.target.files;
	var f = files[0];
	var reader = new FileReader();
	 
	  reader.onload = (function(theFile) {
			return function(e) {
			  document.getElementById('filePreviewResnet').innerHTML = ['<img src="', e.target.result,'" title="', theFile.name, '" width="150" />'].join('');
			};
	  })(f);
	   
	  reader.readAsDataURL(f);
}

function handleCapstoneImageClassificationTrainUpload(evt){
	var files = evt.target.files;
	var f = files[0];
	var reader = new FileReader();
	 
	  reader.onload = (function(theFile) {
			return function(e) {
			  //document.getElementById('filePreviewResnet').innerHTML = ['<img src="', e.target.result,'" title="', theFile.name, '" width="150" />'].join('');
			};
	  })(f);
	   
	  reader.readAsDataURL(f);

}
function handleCapstoneImageClassificationTestUpload(evt){
	var files = evt.target.files;
	var f = files[0];
	var reader = new FileReader();
	 
	  reader.onload = (function(theFile) {
			return function(e) {
			  //document.getElementById('filePreviewResnet').innerHTML = ['<img src="', e.target.result,'" title="', theFile.name, '" width="150" />'].join('');
			};
	  })(f);
	   
	  reader.readAsDataURL(f);

}


$('#capstoneImageTrainUploadBtn').click(uploadAndTrainClassificationUsingResnet);
$('#capstoneImageTestUploadBtn').click(uploadAndTestClassificationUsingResnet);
$('#capstoneImageGenerateTokenBtn').click(generateToken);


document.getElementById('capstoneImageTrainUpload').addEventListener('change', handleCapstoneImageClassificationTrainUpload, false);
document.getElementById('capstoneImageTestUpload').addEventListener('change', handleCapstoneImageClassificationTestUpload, false);


displayhome();
//generators()
//poseestimation()
//nlp_bert()
//nlp_imagecaption()
$(function() {
    $('a.popper').hover(function() {
        $('#pop').toggle();
    });
});

/*
function facerecognition(){
document.getElementById("facerecognition").style.display = "block";
document.getElementById("classification").style.display = "none";
document.getElementById("facealignment").style.display = "block";
document.getElementById("facerecognition").style.display = "block";

document.getElementById("about").style.display = "none";

document.getElementById("poseestimation").style.display = "none";
}
*/



function displayhome(){
	document.getElementById("capstone_image_classification_train_div").style.display = "block";
	document.getElementById("capstone_image_classification_test_div").style.display = "block";
	document.getElementById("capstone_sentimentanalysis_train_div").style.display = "block";
	document.getElementById("capstone_sentimentanalysis_test_div").style.display = "block";
}

function capstone_sentimentanalysis_train(){
	document.getElementById("capstone_image_classification_train_div").style.display = "none";
	document.getElementById("capstone_image_classification_test_div").style.display = "none";
	document.getElementById("capstone_sentimentanalysis_train_div").style.display = "block";
	document.getElementById("capstone_sentimentanalysis_test_div").style.display = "none";
	
}

function capstone_sentimentanalysis_test(){
	document.getElementById("capstone_image_classification_train_div").style.display = "none";
	document.getElementById("capstone_image_classification_test_div").style.display = "none";
	document.getElementById("capstone_sentimentanalysis_train_div").style.display = "none";
	document.getElementById("capstone_sentimentanalysis_test_div").style.display = "block";
	
}

function capstone_classification_train(){
	document.getElementById("capstone_sentimentanalysis_train_div").style.display = "none";
	document.getElementById("capstone_sentimentanalysis_test_div").style.display = "none";
	
	document.getElementById("capstone_image_classification_train_div").style.display = "block";
	document.getElementById("capstone_image_classification_test_div").style.display = "none";
	
}

function capstone_classification_test(){
	document.getElementById("capstone_sentimentanalysis_train_div").style.display = "none";
	document.getElementById("capstone_sentimentanalysis_test_div").style.display = "none";
		
	document.getElementById("capstone_image_classification_train_div").style.display = "none";
	document.getElementById("capstone_image_classification_test_div").style.display = "block";

}

