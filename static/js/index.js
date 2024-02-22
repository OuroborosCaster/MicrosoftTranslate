const app = Vue.createApp({
    data() {
        return {
            languages: {},
            sourceLanguage: 'en',
            targetLanguage: 'zh-Hans',
            sourceText: '',
            targetText: ''
        };
    },
    mounted() {
        fetch('/api/languages')
            .then(response => response.json())
            .then(data => {
                this.languages = data;
                this.updateSelectOptions();
            });

        document.getElementById('swapButton').addEventListener('click', () => {
            this.swapLanguages();
        });
    },
    methods: {
        updateSelectOptions() {
            const sourceSelect = document.getElementById('sourceLanguage');
            const targetSelect = document.getElementById('targetLanguage');

            for (const code in this.languages) {
                const language = this.languages[code];
                sourceSelect.options.add(new Option(language, code));
                targetSelect.options.add(new Option(language, code));
            }

            sourceSelect.value = this.sourceLanguage;
            targetSelect.value = this.targetLanguage;
        },
        expand(event) {
            event.target.style.height = 'auto';
            event.target.style.height = (event.target.scrollHeight) + 'px';
        },
        translate() {
            // 创建一个对象，包含 sourceText、sourceLanguage 和 targetLanguage
            const data = {
                source: this.sourceLanguage,
                target: this.targetLanguage,
                text: this.sourceText
            };

            // 发送 POST 请求
            fetch('/api/translate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            })
                .then(response => response.json())
                .then(data => {
                    // 将返回的 result 赋值给 targetText
                    this.targetText = data.result;

                    // 更新 textarea 的高度
                    this.$nextTick(() => {
                        const textarea = this.$refs.targetTextarea;
                        this.expand({target: textarea});
                    });
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        },
        swapLanguages() {
            [this.sourceLanguage, this.targetLanguage] = [this.targetLanguage, this.sourceLanguage];
            this.updateSelectOptions();
            if (this.targetText) {
                this.sourceText = this.targetText;
                this.$nextTick(() => {
                    const textarea = this.$refs.sourceTextarea;
                    this.expand({target: textarea});
                });
                this.targetText = '';
                this.translate();
            }
        },
    }
}).mount('#app');
