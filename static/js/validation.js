(() => {
    "use strict";

    const forms = document.querySelectorAll(".needs-validation");

    Array.from(forms).forEach((form) => {
        form.addEventListener(
            "submit",
            (event) => {
                const rating = form.querySelector("#id_rating");
                const comment = form.querySelector("#id_comment");

                let customValid = true;

                if (rating) {
                    const ratingValue = Number(rating.value);
                    if (ratingValue < 1 || ratingValue > 5) {
                        rating.setCustomValidity("Rating must be between 1 and 5.");
                        customValid = false;
                    } else {
                        rating.setCustomValidity("");
                    }
                }

                if (comment) {
                    if (comment.value.trim().length < 10) {
                        comment.setCustomValidity(
                            "Review must contain at least 10 characters."
                        );
                        customValid = false;
                    } else {
                        comment.setCustomValidity("");
                    }
                }

                if (!form.checkValidity() || !customValid) {
                    event.preventDefault();
                    event.stopPropagation();
                }

                form.classList.add("was-validated");
            },
            false
        );
    });
})();
