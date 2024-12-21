// // $(document).ready(function () {
// //     $('#qaForm').submit(function (event) {
// //         event.preventDefault(); // Prevent the default form submission
// //         var question = $('#question').val(); // Get the question from the input field
// //         var data = JSON.stringify({ question: question }); // Convert data to JSON format
// //         $.ajax({
// //             type: 'POST',
// //             url: '/conversation',
// //             data: data, // Send JSON data
// //             contentType: 'application/json',  // Set the content type to JSON
// //             success: function (response) {
// //                 $('#responseParagraph').text(response); // Update response paragraph
// //             },
// //             error: function (xhr, status, error) {
// //                 console.log(xhr.responseText);
// //             }
// //         });
// //     });
// // });
// $(document).ready(function () {
//     $('#qaForm').submit(function (event) {
//         event.preventDefault(); // Prevent the default form submission
//         var question = $('#question').val(); // Get the question from the input field
//         var data = JSON.stringify({ question: question }); // Convert data to JSON format
//         $.ajax({
//             type: 'POST',
//             url: '/conversation',
//             data: data, // Send JSON data
//             contentType: 'application/json',  // Set the content type to JSON
//             success: function (response) {
//                 $('#responseParagraph').text(response); // Update response paragraph
//             },
//             error: function (xhr, status, error) {
//                 console.log(xhr.responseText);
//             }
//         });
//     });
// });


$(document).ready(function () {
    $('#qaForm').submit(function (event) {
        event.preventDefault(); // Prevent the default form submission
        var question = $('#question').val(); // Get the question from the input field
        var data = JSON.stringify({ question: question }); // Convert data to JSON format
        $.ajax({
            type: 'POST',
            url: '/conversation',  // Ensure the correct URL for the POST request
            data: data, // Send JSON data
            contentType: 'application/json',  // Set the content type to JSON
            success: function (response) {
                $('#responseParagraph').text(response); // Update response paragraph
            },
            error: function (xhr, status, error) {
                console.log(xhr.responseText);
            }
        });
    });
});
