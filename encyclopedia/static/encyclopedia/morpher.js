document.addEventListener('DOMContentLoaded', function() {
    const button = document.getElementById('morph-button');
    const words = [
        "Science",
        "科学",   // Chinese
        "科学",   // Japanese
        "علوم",   // Arabic
        "מדע",    // Hebrew
        "วิทยาศาสตร์", // Thai
        "Ciência",  // Portuguese
        "Scienza",  // Italian
        "Wissenschaft", // German
        "Sciences",
        "Sience",
        "Sciencia",
        "Sciència",
        "Szyencja",
        "Sciencia",
        "Scienz",
        "Sciença",
        "Sciencia"
    ];

    let currentIndex = 0;

    // Function to morph text
    function morpher(start, end) {
        const chars = "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()".split("");
        const duration = 6;
        const frameRate = 20;

        const textString = start.split("");
        const result = end.split("");
        const slen = textString.length;
        const rlen = result.length;

        let present = new Date();
        let past = present.getTime();
        let count = 0;
        let spentTime = 0;
        const splitTime = (duration * 70) / Math.max(slen, rlen);

        function update() {
            present = new Date();
            spentTime += present.getTime() - past;

            for (let i = count; i < Math.max(slen, rlen); i++) {
                const random = Math.floor(Math.random() * chars.length);
                textString[i] = chars[random];
            }

            if (spentTime >= splitTime) {
                count += Math.floor(spentTime / splitTime);
                for (let j = 0; j < count; j++) {
                    textString[j] = result[j] || "";
                }
                spentTime = 0;
            }

            button.textContent = textString.join("");

            past = present.getTime();

            if (count < Math.max(slen, rlen)) {
                setTimeout(() => {
                    window.requestAnimationFrame(update);
                }, 1000 / frameRate);
            }
        }

        update();
    }

    function startMorphing() {
        let counter = 0;

        setInterval(() => {
            const start = button.textContent;
            const end = words[counter];

            morpher(start, end);

            if (counter < words.length - 1) {
                counter++;
            } else {
                counter = 0;
            }
        }, 3000);
    }

    startMorphing();
});
