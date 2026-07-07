document.addEventListener('DOMContentLoaded', () => {
    const imageUpload = document.getElementById('imageUpload');
    const imagePreview = document.getElementById('imagePreview');
    const imageSection = document.querySelector('.image-section');
    const loader = document.querySelector('.loader');
    const resultDiv = document.getElementById('result');
    const btnPredict = document.getElementById('btn-predict');
    const form = document.getElementById('upload-file');

    imageSection.style.display = 'none';
    loader.style.display = 'none';
    resultDiv.style.display = 'none';

    function readURL(input) {
        if (input.files && input.files[0]) {
            const reader = new FileReader();
            reader.onload = function(e) {
                imagePreview.style.backgroundImage = `url(${e.target.result})`;
                imagePreview.style.display = 'none';
                setTimeout(() => {
                    imagePreview.style.display = 'block';
                    imagePreview.classList.add('fade-in');
                }, 50);
            }
            reader.readAsDataURL(input.files[0]);
        }
    }

    imageUpload.addEventListener('change', function() {
        imageSection.style.display = 'block';
        btnPredict.style.display = 'inline-block';
        resultDiv.textContent = '';
        resultDiv.style.display = 'none';
        readURL(this);
    });

    btnPredict.addEventListener('click', async () => {
        const formData = new FormData(form);

        btnPredict.style.display = 'none';
        loader.style.display = 'block';
        resultDiv.style.display = 'none';

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                body: formData
            });
            const text = await response.text();
            
            loader.style.display = 'none';
            resultDiv.style.display = 'block';
            resultDiv.innerHTML = `<span><strong>${text}</strong></span>`;
            resultDiv.classList.add('fade-in');
        } catch (error) {
            loader.style.display = 'none';
            resultDiv.style.display = 'block';
            resultDiv.innerHTML = `<span>Error: ${error.message}</span>`;
        }
    });
});