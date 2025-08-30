FROM astrocrpublic.azurecr.io/runtime:3.0-9

USER root

# Instalar dependências necessárias para Chrome
RUN apt-get update && apt-get install -y wget gnupg unzip \
    libnss3 libgconf-2-4 libxi6 libxcursor1 libxdamage1 libxrandr2 \
    libasound2 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdbus-1-3 \
    libdrm2 libgbm1 libxcomposite1 libxfixes3 libxrender1 libpango-1.0-0 \
    libpangocairo-1.0-0 fonts-liberation libappindicator3-1 libcurl4 xdg-utils \
    && rm -rf /var/lib/apt/lists/*

# Instalar Google Chrome estável
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" \
    > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && apt-get install -y google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*

# Instalar chromedriver compatível com a versão do Chrome
RUN CHROME_VERSION=$(google-chrome --version | awk '{print $3}' | cut -d'.' -f1) && \
    DRIVER_VERSION=$(wget -qO- "https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_$CHROME_VERSION") && \
    wget -q "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/$DRIVER_VERSION/linux64/chromedriver-linux64.zip" -O /tmp/chromedriver.zip && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
    mv /usr/local/bin/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver && \
    chmod +x /usr/local/bin/chromedriver && \
    rm -rf /tmp/chromedriver.zip /usr/local/bin/chromedriver-linux64

USER astro
