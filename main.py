#import os
import streamlit as st
import time
import streamlit_analytics

import yfinance as yf
import cufflinks as cf
import datetime
import random

random_quotes = [
    [
        "“It might make sense just to get some in case it catches on.”",
        " — Satoshi Nakamoto, 2008",
    ],
    ["“Not your keys, not your Bitcoin”", ""],
    ["“Tick tock, next block”", ""],
    ["“One sat equals one sat”", ""],
    ["“Everyone gets into Bitcoin at the price they diserve”", ""],
]


###### 'sans serif', 'serif', 'monospace'
images_loop = [
    "https://cdn.pixabay.com/photo/2016/11/10/05/25/bitcoin-1813507_960_720.png",
    "https://i.ytimg.com/vi/fsfoqdqyykI/maxresdefault.jpg",
    "https://www.businessinsider.in/photo/23422372/Then-youre-greeted-by-the-main-homepage-Lets-browse-the-psychedelics-.jpg",
    "https://www.wired.com/images_blogs/threatlevel/2011/06/xlarge_0601_silkroadnew.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/2/28/Silk_road_payment.jpg/440px-Silk_road_payment.jpg",
    "data:image/png;base64,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",
    "https://miro.medium.com/v2/resize:fit:1240/0*qP40znARKwtmiwoG.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/0/0b/Silk_Road_Seized.jpg",
    "https://www.china-briefing.com/news/wp-content/uploads/2021/10/China-Makes-Cryptocurrency-Transactions-Illegal-An-Explainer.jpg",
    "https://www.coindesk.com/resizer/iqzu6i1htfcsf67xQpc8iRaNbNw=/1200x600/center/top/cloudfront-us-east-1.images.arcpublishing.com/coindesk/F5CBH7N6L5AFNJL75UT34YUTOE.png",
]

###### Defs
def init_styling():
    button_style = """<style>

        .stButton > button:hover{
        border:none;
        box-shadow: 0 6px 7px 0 rgba(0,0,0,0.24),1px 8px 18px 2px rgba(0,0,0,0.19);
        -webkit-transition-duration: 0.2s; /* Safari */
        transition-duration: 0.2s;
        
        }
        </style>
        """
    st.markdown(button_style, unsafe_allow_html=True)

def hide_anchor_link():
    st.markdown(
        """
    <style>
    /* Hide the link button */
    .stApp a:first-child {
        display: none;
    }
    
    .css-15zrgzn {display: none}
    .css-eczf16 {display: none}
    .css-jn99sy {display: none}
    </style>
    """,
        unsafe_allow_html=True,
    )


def add_exp_section(subheader, text, date, location, more_info):

    col1, col2 = st.columns([6, 2])
    with col1:
        st.subheader(subheader)
    with col2:
        st.caption(date)
    with col1:
        st.write(text)
    with col2:
        if more_info != "":
            button_clicked = st.button("More info...", key=date)
    if more_info != "":
        if button_clicked == True:
            st.write(more_info)
    st.divider()


def add_sk_section(skill, text, most_improved_in, emoji):
    col1, col2 = st.columns([6, 2])
    with col2:
        st.subheader(emoji)
    with col1:
        st.subheader(skill)
        st.write(text)
    with col2:
        st.caption("Developed in " + most_improved_in)
    st.divider()


def add_hk_section(skill, text, stars, emoji):
    col1, col2 = st.columns([6, 2])
    with col2:
        st.subheader(emoji)
    with col1:
        st.subheader(skill)
        st.write(text)
    with col2:
        star_string = ""
        for i in range(stars):
            star_string = star_string + ":star:"
        if stars > 0:
            st.caption("Stars: " + star_string)
    st.divider()


def ai_chatbox(placeholder):

    col1, col2 = st.columns([8, 2])

    with col1:
        usr_prompt = st.text_input(
            "",
            max_chars=100,
            placeholder=placeholder,
            label_visibility="collapsed",
        )
    ###### Number of people
    with col2:
        search = st.button("**Ask the AI**", type="secondary")

    if usr_prompt == "":
        ### Question Suggestions
        st.write("You can ask things like: ")
        if st.button(
            "How would Enrique perform if asked to create a Business Plan for a new Cologne?"
        ):
            usr_prompt = "How would Enrique perform if asked to create a Business Plan for a new Cologne?"
        if st.button(
            "How would Enrique perform when leading a team of 5 senior program managers?"
        ):
            usr_prompt = "How would Enrique perform when leading a team of 5 senior program managers?"
        st.divider()
    if usr_prompt:
        st.caption("Question: " + usr_prompt)
    ###### Prompt templates


def charts(ticker="BTC", scale="log"):  ## log or lineal
    ########## BTC Price Action
    # Sidebar
    [col1, col2, col3, col4] = st.columns(4)

    start_date = col1.date_input("Start date", datetime.date(2009, 1, 1))
    end_date = col2.date_input("End date", datetime.date.today())

    # Periods
    period_selector = col3.selectbox(
        "Period", options=("Days", "Weeks", "Months", "Quarters"), index=1
    )
    period_switcher = {"Days": "1d", "Weeks": "1wk", "Months": "1mo", "Quarters": "3mo"}

    # Scale
    index = {"log": 0, "linear": 1}
    scale = col4.selectbox("Scale", options=("log", "linear"), index=index[scale])

    # Retrieving tickers data
    ticker_switcher = {
        "BTC": "BTC-USD",
        "BTCD": "BTCD",
        "M2": "USM2MSSM",
        "S&P500": "^GSPC",
    }
    tickerSymbol = ticker_switcher[ticker]
    tickerData = yf.Ticker(tickerSymbol)  # Get ticker data

    tickerDf = tickerData.history(
        interval=period_switcher[period_selector], start=start_date, end=end_date
    )  # get the historical prices for this ticker

    string_name = tickerData.info["longName"]

    # st.write(tickerDf)
    index = "%s" % string_name
    metric_switcher = {
        "Days": " (Bollinger bands)",
        "Weeks": " (20w SMA)",
        "Months": " (100w, 200w & 300w SMA)",
        "Quarters": "",
    }

    title = index + metric_switcher[period_selector]
    qf = cf.QuantFig(tickerDf, title=title, legend="top", name="GS")

    if period_selector == "Weeks":
        qf.add_sma([20], width=2, color=["grey"], legendgroup=True)
    elif period_selector == "Days":
        qf.add_bollinger_bands(colors="grey")
    elif period_selector == "Months":
        qf.add_sma(
            [
                int((300 / 52) * 12),
                int((200 / 52) * 12),
                int((100 / 52) * 12),
            ],
            width=1,
            color=["grey", "grey", "grey"],
            legendgroup=True,
        )

    fig = qf.iplot(
        kind="candle",
        up_color="green",
        down_color="red",
        asFigure=True,
        yaxis_type=scale,
    )

    # fig["layout"].update({"xaxis": {"type": "log"}})
    # fig.update_layout(yaxis_type="log")
    #
    st.plotly_chart(fig)

    ####
    # st.write('---')
    # st.write(tickerData.info)

    ######### BTC Price Action END


def fear_greed_index():
    [col1, col2, col3, col4] = st.columns([2, 16, 8, 2])
    with col2:
        st.image("https://alternative.me/crypto/fear-and-greed-index.png", width=350)
    with col3:
        st.markdown("")
        st.markdown("")
        st.markdown("")
        st.markdown("")
        st.info(
            "\n Metric based on Volatility, momentum, social media, dominance and trends."
            + "\n"
            + "\n"
            + "\n"
            + "[Link](https://alternative.me/crypto/fear-and-greed-index/)"
        )


def image_explained(path, text, link):
    [col1, col2, col3, col4] = st.columns([2, 16, 8, 2])
    with col2:
        st.image(path, width=350)
    with col3:
        st.markdown("")
        st.markdown("")

        st.info(text + "\n" + "\n" + "\n" + "[Link](" + link + ")")


def img_loop(images, seconds):

    with st.empty():
        for img in images:
            # st.image(img,use_column_width=True)
            st.markdown(
                "<center><img src=" + img + " width=600></center>",
                unsafe_allow_html=True,
            )
            time.sleep(seconds)


# Menus
def p_subtitle(subtitle):
    st.write("""<h4>%s</h4>""" % subtitle, unsafe_allow_html=True)


def p_titles(p_title, p_subtitle):
    with title.container():
        [col1, col2, col3] = st.columns([4, 20, 4])
        with col2:
            st.write(
                """<h2><center>%s</center></h2>""" % p_title,
                unsafe_allow_html=True,
            )
            st.write(
                """<h4><center>%s</center></h4>""" % p_subtitle,
                unsafe_allow_html=True,
            )
        with col1:
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            p_buttons("Home", "home")
        st.divider()


def p_buttons(name, page):
    button_press = st.button(name, key=page, type="primary")
    if button_press == True:
        st.session_state["page"] = page
        st.session_state["sidebar_tools_state"] = "normal"
        st.experimental_rerun()


def quote(text):
    [col1, col2, col3] = st.columns([1, 18, 1])
    col2.write("""— %s —""" % text)


def rand_quote(placeholder_quotes):
    with placeholder_quotes:
        if "ran" not in st.session_state:
            st.session_state["ran"] = -1
        ran1 = random.randint(0, len(random_quotes) - 1)
        if ran1 == st.session_state["ran"]:
            if ran1 == 0:
                st.session_state["ran"] = 1
            else:
                st.session_state.ran = st.session_state.ran - 1
        else:
            st.session_state["ran"] = ran1
        st.sidebar.write(random_quotes[st.session_state["ran"]][0])
        st.sidebar.write(random_quotes[st.session_state["ran"]][1])


# Pages
def t_scenario():
    p_titles("Tools", "Scenario Analysis")

    add_investments()
    charts()
    fear_greed_index()


def p_immutability():
    p_titles("Immutability", "Storing value through time")
    st.image("https://dergigi.com/assets/images/bitcoin-is-time.jpg")
    [col1, col2] = st.columns([6, 2])
    with col2:
        st.caption(
            "Bitcoin is time - Dergigi [Link](https://dergigi.com/2021/01/14/bitcoin-is-time/)"
        )
    quote(
        "“Anything that can go wrong will go wrong.” - Murphy's law. [Link](https://en.wikipedia.org/wiki/Murphy%27s_law)"
    )
    st.write(
        """We've talked about how Bitcoin removed counterparty risk. But... **what about more explicit risks**? How does Bitcoin protect against bugs or attacks on the network for example?"""
    )
    st.write(
        "Given that we are talking about a revolutionary technology that is already changing the world, you might not expect this simple line of defense:"
    )

    st.write(
        """<center>The Integrity, Philosophy and Culture amongst the community and developers</center>""",
        unsafe_allow_html=True,
    )
    st.write("")
    st.write(
        "Don't get me wrong, Bitcoin's network security is not made out of love, faith, and butterflies. There is a strong consensus mechanism that shields against attacks or fraud within the network (Proof of Work)."
    )
    st.write(
        "However, bugs happen ([CVE-2018-17144](https://bitcoincore.org/en/2018/09/20/notice/)), which is why the biggest risks come from changing the code. Deliverate attempts at passing potentially harmful updates have also happened, and will likely happen again ([Block size wars](https://blog.bitmex.com/?s=block+size+war&lang=en_us))."
    )

    st.info(
        """The two **highest potential risks** come from:
            
1. **Human errors**, either during development or during decision taking.
            
2. **Misconception or misalignment** on what makes Bitcoin valuable.""",
        icon="💡",
    )
    st.write("For this reason,")
    st.info(
        "A **strict working methodology and conservative decision taking** are paramount on the developer side. While on the community side, **education and honest conversations** are the key to alignment",
        icon="💡",
    )
    st.markdown(
        """<center><iframe src="https://i.giphy.com/media/nTfdeBvfgzV26zjoFP/giphy.webp" width="480" height="480" frameBorder="0" ></iframe></center>""",
        unsafe_allow_html=True,
    )
    st.write(
        "Wait a second... If the value of Bitcoin comes from eliminating risk, but you're now telling me that there are known risks. Shouldn't this eliminate or at least reduce its value?"
    )
    st.write(
        "Yes, it certainly does reduce its value. However, it has a proven track record of resilience to both human error and externalities. "
    )
    st.info(
        """At the end of the day, finance is all about probabilties of outcomes and their impact. Bitcoin has a great potential to increase its value over time, and a small probability of failing tremendously. Other assets have almost zero to none growth potential, and a huge probability of losing value slowly
    
- A scenario analysis can be a great way of assessing these choices by adjusting their potential value based on the possible outcomes""",
        icon="💡",
    )
    st.subheader("Scenario risk analysis")
    add_investments()


def p_shadows():
    p_titles("Crime and Chaos", "Shadows emerge")

    st.write(
        """
**Chapter 1: The Silk Road Unveiled (2013)**

In the underbelly of the internet, a hidden marketplace known as the Silk Road and born in 2011, emerged like a shadowy specter. The year was 2013, and its founder, Ross Ulbricht, operated under the pseudonym Dread Pirate Roberts. The Silk Road allowed users to trade illicit goods using the newfound anonymity of Bitcoin. As law enforcement struggled to penetrate its encrypted layers, a veil of crime and chaos began to cast its shadow.

**Chapter 2: The Demise of Silk Road (2013-2014)**

As the Silk Road's operations continued to flourish, a relentless investigation by law enforcement closed in on its operator, Ross Ulbricht. In October 2013, Ulbricht was arrested, his dark web empire finally exposed to the light. The notorious marketplace's downfall sent shockwaves through the criminal underbelly of the internet, casting a stark reminder that digital anonymity had its limits.
"""
    )
    [col1, col2, col3] = st.columns([1, 2, 1])
    with col2:
        st.image(
            "https://upload.wikimedia.org/wikipedia/commons/0/0b/Silk_Road_Seized.jpg",
            width=300,
        )
    st.write(
        """
**Chapter 3: China's Regulatory Quakes (2013-2014)**

From the far east, a new storm emerged. China, once a hotspot for Bitcoin mining and trading, witnessed the government's tightening grip on the cryptocurrency landscape. In 2013, the People's Bank of China prohibited financial institutions from dealing with Bitcoin. The following year, China's central bank took further steps to stifle cryptocurrency activities, casting a cloud of uncertainty over the global Bitcoin community.
"""
    )
    [col1, col2, col3] = st.columns([1, 2, 1])
    with col2:
        st.image(
            "https://www.china-briefing.com/news/wp-content/uploads/2021/10/China-Makes-Cryptocurrency-Transactions-Illegal-An-Explainer.jpg",
            width=300,
        )
    st.write(
        """
**Chapter 4: The Mt. Gox Disaster (2014)**

In the heart of the Bitcoin world, an impending disaster loomed. Mt. Gox, once the largest Bitcoin exchange, revealed a gaping hole in its security. In early 2014, the exchange suspended withdrawals, citing a "bug" in the system. As weeks turned into months, users' fears were realized – Mt. Gox had suffered a massive hack, resulting in the loss of 850,000 Bitcoins. The incident sent shockwaves through the ecosystem, a reminder of the nascent industry's vulnerabilities.


**Epilogue: Shadows to Light**

In the years 2013 to 2014, the shadow cast upon Bitcoin's trajectory was a blend of criminal activity, regulatory uncertainty, and technological vulnerability. As the cryptocurrency emerged from the murkiness, it faced the challenge of steering its narrative away from the shadows that had clung to its name. The rollercoaster of events had revealed both its potential and its pitfalls, leaving the world to wonder if Bitcoin could transcend its tumultuous origins and emerge into the light of mainstream acceptance."""
    )


def p_baby():  # https://cryptonews.net/editorial/press-releases/hidden-messages-found-on-the-bitcoin-blockchain/#:~:text=Bitcoin%27s%20most%20popular%20message%20is,of%20second%20bailout%20for%20banks.%22
    p_titles("Genesis:", "In the fire of corruption, a new hope is born")
    st.write(
        """
**Chapter 1: Genesis of an Idea (2008)**

In the dark corners of the internet, an enigmatic figure known as Satoshi Nakamoto unveiled a revolutionary concept. In a whitepaper titled "Bitcoin: A Peer-to-Peer Electronic Cash System," Nakamoto introduced the world to a digital currency that bypassed traditional banks, a currency operated by a decentralized network. With the world grappling with financial crises, this mysterious visionary gave birth to a seed of possibility.

**Chapter 2: The Dawn of Bitcoin (2009)**

The year 2009 saw the inception of Bitcoin's journey. Satoshi Nakamoto, shrouded in anonymity, mined the first block of the blockchain – the Genesis Block. A message within its code spoke of a system designed to challenge the status quo of finance. As the world slept, Bitcoin began its quiet ascent, a digital entity with untold potential.
"""
    )
    [col1, col2, col3, col4] = st.columns([2, 36, 5, 2])
    with col2:
        hex_string = st.text_input(
            """🕵️ Use the [BlockExplorer](https://blockstream.info/block/000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f), 
            to find the Hexadecimal code in the signature of the Genesis block and paste it here to transcribe it""",
            help="It's the code beside 	OP_PUSHBYTES_4 ffff001d OP_PUSHBYTES_1 04 OP_PUSHBYTES_69 in the SCRIPTSIG (ASM) part",
            placeholder="Paste Hexadecimal code here",
        )
        byte_string = bytes.fromhex(hex_string)
        ascii_string = byte_string.decode("ASCII")
    with col3:
        st.write("")
        st.write("")
        st.write("")
        button_skip = st.button("Skip")
    [col1, col2, col4] = st.columns([2, 41, 2])
    with col2:
        if "Chancellor on brink of second bailout" in ascii_string:
            st.info(
                "["
                + ascii_string
                + "](https://12ft.io/proxy?&q=https%3A%2F%2Fwww.thetimes.co.uk%2Farticle%2Fchancellor-alistair-darling-on-brink-of-second-bailout-for-banks-n9l382mn62h)",
                icon="💡",
            )
        elif button_skip:
            st.info(
                "["
                + "The Times 03/Jan/2009 Chancellor on brink of second bailout for banks"
                + "](https://12ft.io/proxy?&q=https%3A%2F%2Fwww.thetimes.co.uk%2Farticle%2Fchancellor-alistair-darling-on-brink-of-second-bailout-for-banks-n9l382mn62h)",
                icon="💡",
            )
        elif not hex_string:
            hex_string = ""
        else:
            st.warning(ascii_string, icon="⚠️")
    st.write(
        """
**Chapter 3: The First Ripples (2010)**

Bitcoin's ripple effect touched reality in 2010. Laszlo Hanyecz, a programmer with a sense of adventure, made history by trading 10,000 Bitcoins for two pizzas – a modest transaction that ignited the first sparks of a currency's tangible value. The seeds of curiosity were sown, as whispers of a new way of conducting transactions began to spread. This day became known as **Bitcoin pizza day**.

**Chapter 4: Emergence of Exchanges (2010)**

As 2010 unfolded, a virtual marketplace emerged from unlikely origins. Mt. Gox, born from the world of trading Magic: The Gathering cards, embraced Bitcoin, laying the groundwork for what would become one of the most influential cryptocurrency exchanges. It was here that traders first haggled over the nascent digital currency, shaping its first interactions with the world of finance.
"""
    )
    image_explained(
        "https://upload.wikimedia.org/wikipedia/commons/d/dc/MtGox.png",
        "Magic The Gathering Online eXchange",
        "https://en.wikipedia.org/wiki/Mt._Gox",
    )

    st.write(
        """
**Chapter 5: Challenges and Controversies (2011-2012)**

With innovation came challenges. The early years of Bitcoin were marked by skirmishes within its own ranks. Amid discussions about its potential, debates over the optimal block size raged, foreshadowing the divisive "block size wars" to come. Yet, through turmoil, the resilient cryptocurrency continued to evolve, its promise undeterred by internal strife.

**Epilogue: A Glimpse of the Future**

In the shadow of traditional financial systems, a new currency emerged, born from the mind of an enigmatic figure and nurtured by a growing community of believers. Bitcoin's initial years were marked by a mix of hope, experimentation, and skepticism. Little did the world know that this digital marvel would spark a revolution, transforming the very foundations of money, trust, and the way we exchange value. As Bitcoin ventured into the uncharted waters of the future, it carried with it the potential to rewrite the story of economics, finance, and states."""
    )


def p_journey():
    btcTicker = yf.Ticker("BTC-USD")  # Get ticker data
    btcMarketcap = btcTicker.info["marketCap"]
    p_titles(
        "A long journey",
        "From $0 to $" + str(int(btcMarketcap / 1000000000) / 1000) + " trillion",
    )
    st.write(
        """
1. **Whitepaper Release (2008)**:
   In October 2008, an individual or group using the pseudonym Satoshi Nakamoto published the Bitcoin whitepaper titled "Bitcoin: A Peer-to-Peer Electronic Cash System." This marked the conceptual beginning of Bitcoin as a decentralized digital currency.

2. **Genesis Block (2009)**:
   On January 3, 2009, the first block of the Bitcoin blockchain, known as the "genesis block" or "Block 0," was mined by Satoshi Nakamoto. This block contained the message "The Times 03/Jan/2009 Chancellor on brink of second bailout for banks," referencing the economic context of its creation.

3. **Bitcoin Pizza Day: First Bitcoin Transaction (2010)**:
   On May 22, 2010, programmer Laszlo Hanyecz famously made the first documented real-world transaction using Bitcoin. He purchased two pizzas for 10,000 BTC, illustrating the value of Bitcoin as a medium of exchange.

4. **Mt. Gox Launch (2010)**:
   The Mt. Gox exchange, originally established as a platform for trading Magic: The Gathering cards, began trading Bitcoin in July 2010. It would go on to become one of the most prominent Bitcoin exchanges but later suffered a major hack in 2014.

5. **First Bitcoin Halving (2012)**:
   Bitcoin's block reward halves, from 50 to 25 BTC

6. **Silk Road Shutdown (2013)**:
   The Silk Road, an online marketplace known for illegal activities, was shut down by authorities in October 2013. The seizure of the platform highlighted Bitcoin's use in facilitating illicit transactions.

7. **China's Bitcoin Bans (2013, 2017)**:
   China's government issued bans on financial institutions using Bitcoin in 2013 and later imposed more comprehensive bans on cryptocurrency exchanges and Initial Coin Offerings (ICOs) in 2017, impacting the global cryptocurrency market.

8. **Block Size Debate Emerges (2010-2014)**:
   The community debated increasing the block size limit to accommodate more transactions, highlighting scalability and decentralization concerns.

9. **BIP 100, BIP 101, and BIP 102 (2015)**:
   Proposed BIPs suggested various approaches to increasing the block size limit, sparking intense discussion.

10. **Bitcoin XT Fork Controversy (2015)**:
    The Bitcoin XT fork proposed a larger block size limit, leading to a contentious debate over control and centralization.

11. **Bitcoin Unlimited and Emergent Consensus (2016)**:
    Bitcoin Unlimited provided an alternative solution allowing miners to choose their block sizes based on the concept of Emergent Consensus.

12. **Segregated Witness (SegWit) Activation (2017)**:
    SegWit separated transaction signature data from blocks, increasing transaction capacity without a direct block size increase.

13. **Bitcoin Cash Hard Fork (2017)**:
    Bitcoin Cash emerged as a separate cryptocurrency with an increased block size limit, stemming from disagreements over scaling.

14. **SegWit2x Controversy and Cancellation (2017)**:
    The proposed SegWit2x hard fork aimed to combine SegWit and a block size increase, but it was ultimately abandoned due to lack of consensus.

15. **Bitcoin Cash and Bitcoin SV Forks (2018)**:
    Bitcoin Cash experienced a hard fork leading to the creation of Bitcoin SV, emphasizing larger block sizes and the original vision of Bitcoin.

16. **All-Time High Price (2017)**:
    Bitcoin's price surged to nearly $20,000 in December 2017, drawing attention and investment.

17. **Blockstream's Lightning Network (Ongoing)**:
    The Lightning Network introduced off-chain transactions as a scaling solution, enabling faster and cheaper payments.

18. **Institutional Interest (2020-2021)**:
    Institutional investors and companies began acknowledging Bitcoin as a legitimate asset class.

19. **Elon Musk and Tesla's Involvement (2021)**:
    Tesla's investment in Bitcoin and subsequent reversal on accepting it as payment highlighted the cryptocurrency's volatility.

20. **Bitcoin as Legal Tender in El Salvador (2021)**:
    El Salvador became the first country to adopt Bitcoin as legal tender.

"""
    )


def p_scarcity():
    p_titles("Scarcity", "Increasing value by fixing supply")
    [col0, col1, col2] = st.columns([1, 10, 30])
    with col1:
        st.image(
            "https://d2tt46f3mh26nl.cloudfront.net/public/Lots/202307-1613-4111-05f10503-7cdf-48ee-8faf-31504598618b/SF00000246561copy__1358525f-bbdb-4bf4-a4c8-9e28aa5cbd96@1x",
            width=150,
        )
    with col2:

        quote(
            """In November 2020, a pokemon card 'Shadowless Charizard' was sold for \$369,000. Another copy was sold in 2021 for \$300,000, and another one in 2022 for \$420,000. [Link](https://www.dicebreaker.com/games/pokemon-trading-card-game/best-games/rare-pokemon-cards) 
            """
        )
        st.write(
            """<center>Why?</center>""",
            unsafe_allow_html=True,
        )
        st.write("")
        st.write(
            "Not only it's a first edition of a valued pokemon, but it's also holographic. It also turns out that the first batch had a printing error, so the Charizard was missing its shadow. All of these coincidences make these cards very rare or **scarce**"
        )
    st.write(
        """From this point onwards, it's just good old **supply and demand** balancing: Imagine there are only 5 Charizards in the world (Supply), this means there can only be 5 buyers at a time, but there are thousands of Pokemon fans that want a Charizard. This means that:
1. You must bid enough so that one of the 5 owners is willing to sell
2. You must be at least in the top 5 bidders
3. 8.8\% of adults in USA are millionaires, so there is a high chance that you will be competing with millionaire fans [Link](https://www.zippia.com/advice/millionaire-statistics/#:~:text=There%20are%20about%2022%20million,of%20the%20total%20U.S.%20population.)

Add this together and you find'll yourself paying \$420,000 for a card wich doesn't have any value. """
    )
    st.write(
        """<center><b>Or does it...?</b></center>""",
        unsafe_allow_html=True,
    )
    st.write("")
    st.write(
        "You are a Pokemon super-fan, but you're not stupid. You understand the Pokemon ecosystem, and know that, each year, the number of fans increases by 20%"
    )
    st.write(
        "You also know that, on average, the wealth in the US grows by 6%. You also have contacts on the sphere and know that 2 of the 5 buyers will not sell their Charizards by any means"
    )
    st.write(
        "And finally, you know that you can keep the card from degrading, and avoid the passing of time (**Immutability**). And keep it safely stored by yourself (**No counterparty risk**)"
    )
    st.write(
        """<center><b>Bingo!</b></center>""",
        unsafe_allow_html=True,
    )
    st.write(
        """After 4 years:
1. Supposing there were 10,000 initial super fans, **there are now 20,736 super fans**
2. There are now  only 3 of the 5 Charizards on sale (Including yours)
3. The US population is 21.6\% wealthier
"""
    )
    st.info(
        """The value added comes from the supply:
1. Since there are only 5 Charizards, you will at least opt for the top 5 bidders, sometimes higher if other owners don't sell.

But only if there is a growing demand or groing wealth in the demand:

2. If demand and wealth increases you have higher chances of getting richer buyers. If demand and wealth decrease, your chances of richer buyers are lower""",
        icon="💡",
    )
    st.write(
        "This means, that you are automatically opting for the top 3 bidders. Additionally, since there are double the fans, there are double the chances of finding a wealthier millionaire. And on top of that, those millionaires are 21.5\% richer now"
    )
    st.write(
        "In this environment, the chances of selling the Charizard for \$1,000,000 are very reasonable"
    )
    st.info(
        """Bitcoin's fixed supply makes it the scarcest asset in the world, there will never be more than 21,000,000.

In 2022 there were an estimated 219,000,000 owners of Bitcoin from 183,000,000 at the start of the year. A 19.67\% yearly increase in the 'number of fans'. [Link](https://news.bitcoin.com/report-crypto-adoption-hits-new-milestones-global-crypto-owners-reached-425-million-in-2022/#)

While global GDP (A measure of aconomic output) grew 4,88\%. [Link](https://www.statista.com/statistics/268750/global-gross-domestic-product-gdp/)
        """,
        icon="💡",
    )
    [col1, col2, col3] = st.columns([1, 18, 1])
    st.write("")
    col2.write(
        """**Interesting Fact**: What happens if the high price of Charizard cards attracts the attention of new thousands of fans?

And what if the Charizard owners see this, and start keeping their Charizards for themselves, and only selling them 1 by 1 to get always the highest bidder?

This will increase the price a lot, and in turn attract more fans. These fans will increase the bid for Charizards, which attracts more fans... Creating whats called a 'parabolic rally'.

At some point the Charizard owners realize the new millionaire fans are paying way more than the can afford for the Charizards (A bubble in the market). 
This is when Charizard owners sell their cards at once in fear that they will not get buyers.

This scares the fans, who stop buyin Charizards, and the price collapses, giving birth to a 'bear market'. Which eventualy heals itself into an 'accummulation phase'

This is how Bitcoin cycles work [learn more about cycles🥕](https://www.youtube.com/watch?v=AsT55mpG_G0)"""
    )
    st.write(
        "An interesting way to visualize this dynamic is with the 'Fear and Greed index'"
    )
    fear_greed_index()


def p_decentrelization():
    p_titles("Decentralization", "Adding value by removing risk")

    st.write(
        """Decentralization can sound like a buzzword or an ambiguous concept, but in our case it's just a means to an end: **Removing counterparty risk**."""
    )
    st.write(
        """Have you ever lent your car to some friends? They might break it, but **accidents happen**... and you know them enough to **trust** them.
    """
    )
    [col1, col2, col3] = st.columns([1, 18, 1])
    col2.write(
        """— In 2013, two banks in Cyprus had an **'accident'**, and seized 47.5% of all bank deposits above €100,000 to fix it. [Link](https://en.wikipedia.org/wiki/2012–2013_Cypriot_financial_crisis#:~:text=No%20insured%20deposit%20of%20€,above%20€100%2C000%20were%20seized.) —"""
    )

    st.write("")
    st.write(
        """Whether the seazing of funds in Cyprus was a good or a bad move doesn't matter, what matters is that you have to **trust** the bank to not have **'accidents'** and **trust** that the goverment will choose your side when these **'accidents'** occur."""
    )

    st.info(
        """Problem number 1: **Trust** has inherent **risk**""",
        icon="💡",
    )
    st.write(
        """**Permissions** also rely on **trust**. For example, we **trust** the government to handle **permissions** correctly when it comes to criminals.
    """
    )
    [col1, col2, col3] = st.columns([1, 18, 1])
    col2.write(
        """— A Spanish law was passed on October 7th, 2022. It aimed at reducing the criteria for an act to be considered as rape. 
        Some people argued that the las was against the presumption of innocence, and unconstitutional [Link1](https://www.bbc.com/mundo/noticias-internacional-62694510).
        Additionally, due to the way it was redacted, some offenders had their sentence time reduced or were released from jail [Link2](https://www.elmundo.es/espana/2022/12/01/6388ed8ee4d4d8e8558b4572.html). —"""
    )
    st.write(
        """Again, whether this is good, bad or just a mistake doesn't matter, what matters is that there is **risk** involved"""
    )
    st.info(
        """Problem number 2: **Permissions** require **trust**, which again, carries a **risk**""",
        icon="💡",
    )
    st.write(
        """Decentralization **removes the middlemen** (Banks, institutions...). <b>No middlemen</b> means no <b>trust</b> required, which means no <b>risk</b>.""",
        unsafe_allow_html=True,
    )

    st.write(
        "This risk is called **counterparty risk**. It applies to parties that may not fullfill their part of the agreement."
    )
    st.info(
        """
         \n When it comes to money, savings and transactions, **thanks to it's decentralization, Bitcoin removes this risk**. Removing risk of loss is valuable.""",
        icon="💡",
    )
    st.write("")
    st.write(
        "<left>But look, you're talking about ambiguous concepts, trust, risk... It all sounds like smoke to me, give me a real example which mesures this value.</left>",
        unsafe_allow_html=True,
    )
    [col1, col2, col3] = st.columns([1, 18, 1])
    col2.write(
        """— Credit card companies, such as Visa or Mastercard charge anywhere from 1.5% to 3.5% to merchants whenever you buy something [Link](https://www.fool.com/the-ascent/research/average-credit-card-processing-fees-costs-america/).
         They need to do so because they have at least 7 types of risks that they have to mitigate. 
         While, at the time of writing, a bitcoin transaction costs 0.76$ [Link](https://bitinfocharts.com/comparison/bitcoin-transactionfees.html#3y) —"""
    )
    st.write(
        "Because Bitcoin just has the network infrastructure costs, and they don't depend on the amount sent. A 1000 bitcoin transaction or a 1 bitcoin transaction is exactly the same in terms of computation, so it costs the same"
    )
    st.write(
        """This doesn't apply to Visa or Mastercard, whose main cost is the risk of unpayments or hacks. The bigger the transaction, the greater the risk of unpayment. For this reason, sending 1000€ costs 35€ (high risk if unpaid), while sending 10€ just costs 0.35€ (low risk if unpaid)."""
    )
    st.info(
        """So there is clear **value added by Bitcoin** here, if you wanted to pay for something worth 1000€ in a shop, you would save 34.24€ using Bitcoin, **mainly because it's decentralized (so it doesn't have counterparty risk)**""",
        icon="💡",
    )
    with st.expander("Risks taken by Visa or Mastercard"):
        st.write(
            """Visa, as a payment network and financial services company, takes on several types of risks in its operations. Here are some areas where Visa assumes risk:
1. **Fraud Risk:** Visa is exposed to the risk of fraudulent transactions occurring on its network. This could involve unauthorized use of cards, identity theft, or other forms of payment fraud. Visa invests in security measures, fraud detection systems, and risk management practices to mitigate these risks and protect both cardholders and merchants.
2. **Credit Risk:** When a transaction occurs, Visa authorizes the payment based on the available funds or credit limit of the cardholder. There's a risk that cardholders might exceed their credit limits or not have sufficient funds to cover their purchases. In such cases, Visa might not receive the full payment for the transaction.
3. **Merchant Risk:** Visa is also exposed to the risk of merchants failing to deliver goods or services after a transaction has been authorized. If a cardholder disputes a transaction due to non-receipt of goods or services, Visa might have to facilitate chargebacks and refunds, impacting its revenue.
4. **Settlement Risk:** The settlement process involves the movement of funds between banks. There's a risk that one of the banks might fail to meet its settlement obligations, which could disrupt the smooth operation of the payment network. Visa works to ensure the stability and integrity of the settlement process.
5. **Regulatory and Compliance Risk:** Visa operates in multiple countries and is subject to various regulatory requirements and compliance standards. Failing to comply with these regulations can lead to legal and financial consequences. Visa must manage these risks to maintain its reputation and legality.
6. **Operational Risk:** Any disruptions to Visa's technology infrastructure, data breaches, or technical failures can impact the functionality of its network, causing transaction delays or security breaches. These operational risks can affect both cardholders and merchants.
7. **Market Risk:** Fluctuations in currency exchange rates, interest rates, and economic conditions can affect Visa's financial performance, as well as its exposure to risk. For example, if the global economy experiences a downturn, consumer spending might decrease, impacting Visa's transaction volume.
To manage these risks, Visa employs various risk management strategies, invests in security technologies, implements fraud detection mechanisms, maintains strong partnerships with financial institutions, and stays updated on regulatory changes. It's important for Visa to strike a balance between facilitating efficient and secure transactions while also mitigating the risks associated with its payment network. """
        )
    col2.write(
        """**Interesting Fact**: Bitcoin was created in 2008, as a response to all of the banking malpractices and bailouts that happened around the world ✊.
         The government bailed out the banks, making citizens pay for the risk taken by them, without any of the rewards they got for taking that risk.
         But it wasn't new! There have always been people fighting against financial repression carried by dictatorships and corrupt governments... [learn about cypherpunks👨‍🎤](https://en.wikipedia.org/wiki/Cypherpunk#:~:text=A%20cypherpunk%20is%20any%20individual,to%20social%20and%20political%20change.)"""
    )


def p_home():
    with title.container():
        st.write(
            """<h2><center>Welcome to Bitcoin Concepts</center></h2>""",
            unsafe_allow_html=True,
        )
        st.write(
            """<h4><center>Simply-explained concepts surrounding Bitcoin<center></h4>""",
            unsafe_allow_html=True,
        )
        st.divider()
    p_subtitle(
        "Part 1: “Bitcoin has no real-life value”",
    )
    [col1, col2] = st.columns([4, 4])
    with col1:
        p_buttons(
            "Decentralization: Adding value by removing risk",
            "decentralization",
        )
    with col2:
        p_buttons("Scarcity: Increasing value by fixing supply", "scarcity")
    [col1, col2] = st.columns([4, 3])
    with col1:
        p_buttons("Immutability: Storing value through time", "immutability")

    p_subtitle("Part 2: Building hope through chaos (Bitcoin history)")
    [col1, col2] = st.columns([4, 3])
    with col1:
        p_buttons("Genesis: In the fire of corruption, a new hope is born", "baby")
    with col2:
        p_buttons("Crime and Chaos: Shadows emerge", "shadows")

    btcTicker = yf.Ticker("BTC-USD")  # Get ticker data
    btcMarketcap = btcTicker.info["marketCap"]
    #p_buttons(
    #    "A long Journey: From \$0 to \$"
    #    + str(int(btcMarketcap / 1000000000) / 1000)
    #    + " trillion",
    #    "journey",
    #)

    #p_subtitle("Part 3: The Technology")
    #st.write("Coming Soon...")
    [col1, col2, col3] = st.columns([4, 3, 4])


class investment:
    tot_value = 0

    def __init__(self, asset, principal):
        self.asset = asset
        self.principal = principal

    def scenario_form(self, name):
        with st.form("Scenario: " + name):
            chance = st.number_input(
                name + " chance",
                max_value=1.000,
                help="Set the probability of this outcome from 0 to 1 (all probabilities shoud sum 1)",
            )
            growth = st.number_input(
                name + " growth multiplier",
                help="Set the growth multiplier, for example 2x growth fro a 10\% growth, or 0.7x for a 30\% loss",
            )
            value = chance * growth * self.principal
            submitted = st.form_submit_button("Submit " + name)
            if submitted:
                st.session_state[self.asset + name] = value
                self.tot_value = value + self.tot_value

    def tot_value_show(self):
        st.metric(
            self.asset + " investment value",
            value=self.tot_value,
            delta=str(int((self.tot_value / self.principal - 1) * 10000) / 100) + "%",
        )


def add_investments():
    val1 = 0
    val2 = 0
    val3 = 0
    inv1 = investment(
        st.text_input(
            "Name of the asset",
            key="asset1",
            help="Name the Asset or investment that you want to anayse (Example: Bitcoin)",
        ),
        st.number_input(
            "Investment quantity",
            key="principal1",
            help="Set amount of capital that you plan on investing)",
        ),
    )
    [col1, col2, col3] = st.columns(3)
    with col1:
        input_scenario1 = st.text_input(
            "Name of the scenario 1",
            key=1,
            help="Name the first scenario (Example: 2x Growth)",
        )
        inv1.scenario_form(input_scenario1)
        if inv1.asset + input_scenario1 in st.session_state:
            st.metric(
                "Value added - Scenario: " + input_scenario1,
                value=st.session_state[inv1.asset + input_scenario1],
            )
            val1 = st.session_state[inv1.asset + input_scenario1]
    if input_scenario1:
        with col2:
            input_scenario2 = st.text_input(
                "Name of the scenario 2",
                key=2,
                help="Name the second scenario (Example: Goes to zero)",
            )
            inv1.scenario_form(input_scenario2)
            if inv1.asset + input_scenario2 in st.session_state:
                st.metric(
                    "Value added - Scenario: " + input_scenario2,
                    value=st.session_state[inv1.asset + input_scenario2],
                )
                val2 = st.session_state[inv1.asset + input_scenario2]
        if input_scenario2:
            with col3:
                input_scenario3 = st.text_input(
                    "Name of the scenario 3",
                    key=3,
                    help="Name the third scenario (Example: to 1 million)",
                )
                inv1.scenario_form(input_scenario3)
                if inv1.asset + input_scenario3 in st.session_state:
                    st.metric(
                        "Value added - Scenario: " + input_scenario3,
                        value=st.session_state[inv1.asset + input_scenario3],
                    )
                    val3 = st.session_state[inv1.asset + input_scenario3]
    with col2:
        totl_value = val1 + val2 + val3
        if totl_value != 0:
            st.metric(
                inv1.asset + " investment value",
                value=totl_value,
                delta=str(int((totl_value / inv1.principal - 1) * 10000) / 100) + "%",
            )


###### Hide Menu
if "sidebar_state" not in st.session_state:
    st.session_state["sidebar_state"] = "expanded"

st.set_page_config(
    page_title="ABitCoincept",
    page_icon=":key:",
    #layout="wide",
    initial_sidebar_state=st.session_state.sidebar_state,
)

init_styling()


hide_menu_style = """<style>
.css-1jc7ptx, .e1ewe7hr3, .viewerBadge_container__1QSob, .styles_viewerBadge__1yB5_, .viewerBadge_link__1S137, .viewerBadge_text__1JaDK{ display: none; } #MainMenu{ visibility: hidden; } footer { visibility: hidden; } header { visibility: hidden; }
</style>"""
st.markdown(hide_menu_style, unsafe_allow_html=True)
# hide_anchor_link()
# Main start
# Record analytics
if "new_user" not in st.session_state:
    streamlit_analytics.start_tracking()
    st.session_state["new_user"] = True

## Session state
if "page" not in st.session_state:
    st.session_state["page"] = "home"

# Animations
if st.session_state["page"] == "shadows":
    if "new_shadows" not in st.session_state or st.session_state["new_shadows"] == -2:
        st.session_state.sidebar_state = "collapsed"
        conti = st.button("Are you ready?")
        #conti = True
        st.image("https://hexcol.com/ffffff-og.png")
        st.image("https://hexcol.com/ffffff-og.png")
        st.image("https://hexcol.com/ffffff-og.png")
        st.session_state["new_shadows"] = -2
        if conti:
            st.session_state["new_shadows"] = -1
            st.experimental_rerun()
        st.experimental_rerun()
    elif st.session_state["new_shadows"] == -1:
        img_loop(images_loop, 0.4)
        st.session_state["new_shadows"] = 6

        st.experimental_rerun()

    elif st.session_state["new_shadows"] == 6:
        st.image(
            "https://buybitcoinworldwide.com/pages/info/hacks/money.png",
        )
        st.session_state["new_shadows"] = 7
        time.sleep(3)
        st.experimental_rerun()
    elif st.session_state["new_shadows"] == 7:
        cont = st.button("Continue...")
        if cont:
            st.session_state["new_shadows"] = 8
            st.session_state.sidebar_state = "expanded"
            st.experimental_rerun()

# https://www.coindesk.com/resizer/iqzu6i1htfcsf67xQpc8iRaNbNw=/1200x600/center/top/cloudfront-us-east-1.images.arcpublishing.com/coindesk/F5CBH7N6L5AFNJL75UT34YUTOE.png
# st.session_state.sidebar_state = "expanded"

# Side bar
st.sidebar.write("<h4><center>A Bit Concept</center></h4>", unsafe_allow_html=True)
# if st.session_state["page"] == "shadows":

# st.sidebar.image("""https://cdn-icons-png.flaticon.com/512/991/991959.png""")

st.sidebar.image("resources/bitcoin_logo.png")
placeholder_quotes = st.empty()
rand_quote(placeholder_quotes)

# click_quote_sb = st.sidebar.button("Random Quote", key="quote", type="secondary")


if "sidebar_tools_state" not in st.session_state:
    st.session_state["sidebar_tools_state"] = "normal"
if st.session_state["sidebar_tools_state"] == "normal":
    click_tool_sb = st.sidebar.button("- Tool List", key="side_tools", type="secondary")
    if click_tool_sb:
        st.session_state["sidebar_tools_state"] = "tools"
        st.experimental_rerun()
elif st.session_state["sidebar_tools_state"] == "tools":
    click_tool_sb_scenario = st.sidebar.button(
        "Scenario analysis tool", key="side_tools_scenario", type="secondary"
    )
    if click_tool_sb_scenario:
        st.session_state["sidebar_tools_state"] = "normal"
        st.session_state["page"] = "side_tools_scenario"
        st.experimental_rerun()


# Titel init
title = st.empty()

# Page switch
if st.session_state["page"] == "home":
    p_home()
elif st.session_state["page"] == "decentralization":
    p_decentrelization()
elif st.session_state["page"] == "scarcity":
    p_scarcity()
elif st.session_state["page"] == "journey":
    p_journey()
elif st.session_state["page"] == "baby":
    p_baby()
elif st.session_state["page"] == "shadows":
    if st.session_state["new_shadows"] == 8:
        p_shadows()
elif st.session_state["page"] == "immutability":
    p_immutability()
elif st.session_state["page"] == "side_tools_scenario":
    t_scenario()
# Stop Recording analytics SEE ANALYTICS -> ?analytics=on
if st.session_state["new_user"] == True:
    streamlit_analytics.stop_tracking()
    st.session_state["new_user"] = False
