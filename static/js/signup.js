console.log("Hello world");
const alertBox = document.getElementById("alert-box");
const imageBox = document.getElementById("image-box");
const imageForm = document.getElementById("signup-form");
const confirmBtn = document.getElementById("submit-btn");
const input = document.getElementById("id_profile_picture");

// Form Data
const csrf = document.getElementsByName("csrfmiddlewaretoken");
const username = document.getElementById("id_username");
const email = document.getElementById("id_email");
const password = document.getElementById("id_password");
const first_name = document.getElementById("id_first_name");
const last_name = document.getElementById("id_last_name");

input.addEventListener("change", () => {
  console.log("change");

  const img_data = input.files[0];
  const url = URL.createObjectURL(img_data);
  imageBox.innerHTML = `<img src="${url}" id="image" width="300px">`;

  var $image = $("#image");

  $image.cropper({
    aspectRatio: 1 / 1,
    crop: function (event) {
      console.log(event.detail.x);
      console.log(event.detail.y);
      console.log(event.detail.width);
      console.log(event.detail.height);
      console.log(event.detail.rotate);
      console.log(event.detail.scaleX);
      console.log(event.detail.scaleY);
    },
  });

  // Get the Cropper.js instance after initialized
  var cropper = $image.data("cropper");

  confirmBtn.addEventListener("click", () => {
    cropper.getCroppedCanvas().toBlob((blob) => {
      const fd = new FormData();
      fd.append("csrfmiddlewaretoken", csrf[0].value);
      fd.append("username", username.value);
      fd.append("email", email.value);
      fd.append("password", password.value);
      fd.append("first_name", first_name.value);
      fd.append("last_name", last_name.value);
      fd.append("profile_picture", blob, "my-image.png");

      $.ajax({
        type: "POST",
        url: imageForm.action,
        enctype: "multipart/form-data",
        data: fd,
        success: function (response) {
          console.log("success", response);
        },
        error: function (error) {
          console.log("error:", error);
        },
        cache: false,
        contentType: false,
        processData: false,
      });
    });
  });
});
