# Import for the Web Bot
from botcity.web import WebBot, Browser, By

# Import for integration with BotCity Maestro SDK
from botcity.maestro import *

# Import for integration with BotCity Discord Plugin
from botcity.plugins.discord import BotDiscordPlugin, EmbeddedMessage, Author, Footer, Field, Color


# Disable errors if we are not connected to Maestro
BotMaestroSDK.RAISE_NOT_CONNECTED = False


def main():
    # Runner passes the server url, the id of the task being executed,
    # the access token and the parameters that this task receives (when applicable).
    maestro = BotMaestroSDK.from_sys_args()
    ## Fetch the BotExecution with details from the task, including parameters
    execution = maestro.get_execution()

    try:
        bot = WebBot()

        # Configure whether or not to run on headless mode
        bot.headless = False

        # Uncomment to change the default Browser to Firefox
        bot.browser = Browser.FIREFOX

        # Uncomment to set the WebDriver path
        bot.driver_path = r"C:\Users\diego\Downloads\geckodriver-v0.35.0-win64\geckodriver.exe"

        # Opens the BotCity website.
        bot.browse("https://dev.to")

        #login_devto
        search_article(bot, maestro)

        status =AutomationTaskFinishStatus.SUCCESS,
        message="Task Finished OK."
        
        # Wait 3 seconds before closing
        bot.wait(3000)
    
    except Exception as error:
        maestro.error(task_id=execution.task_id, exception=error)

        status =AutomationTaskFinishStatus.FAILED,
        message="Task failed."
    
    finally:
        bot.stop_browser()
        # Uncomment to mark this task as finished on BotMaestro
        maestro.finish_task(
            task_id=execution.task_id,
            status=AutomationTaskFinishStatus.SUCCESS,
            message="Task Finished OK."
        )




    # Implement here your logic...
    ...

def login_devto(bot: WebBot, maestro: BotMaestroSDK):
            login = bot.find_element('/html/body/header/div/div[2]/div/span/a', By.XPATH)
            login.click()

            email = bot.find_element("user_email", By.ID)
            email.send_keys("email")

            password = bot.find_element("user_password", By.ID)
            password.send_keys("password")

            bot.enter()
            bot.wait(2000)

def search_article(bot: WebBot, maestro: BotMaestroSDK):
        search =  bot.find_element("search-input", By.ID)
        search.send_keys("python")

        bot.enter()

        newest = bot.find_element("/html/body/div[6]/div/main/div/div[1]/nav[1]/ul/li[2]/a", By.XPATH)
        newest.click()

        bot.wait(2000)
        
        author_name = bot.find_element("/html/body/div[6]/div/main/div/div[3]/div[2]/article[1]/div/div/div[1]/div/div[2]/div/div", By.XPATH).text
        article_title = bot.find_element("/html/body/div[6]/div/main/div/div[3]/div[2]/article[1]/div/div/div[2]/h3", By.XPATH).text
        article_link = bot.find_element('/html/body/div[6]/div/main/div/div[3]/div[2]/article[1]/div/div/div[2]/h3/a', By.XPATH).get_attribute("href")
        article_date = bot.find_element("/html/body/div[6]/div/main/div/div[3]/div[2]/article[1]/div/div/div[1]/div/div[2]/a/time", By.XPATH).text
        time_read = bot.find_element("/html/body/div[6]/div/main/div/div[3]/div[2]/article[1]/div/div/div[2]/div[2]/div[2]/small", By.XPATH).text

        bot.wait(2000)

        send_message(author_name, article_title, article_link, article_date, time_read)

def send_message(author_name, article_title, article_link, article_date, time_read):
        url = 'https://discord.com/api/webhooks/my-webhook-url'
        discord = BotDiscordPlugin(urls= url, username= "Captain Hook")

        # Instanciando a mensagem incorporada
        mensagem = EmbeddedMessage (
            title = article_title,
            description = '',
            color = Color.BLUE
        )

        # Defina o autor
        mensagem.author = Author(
            name = author_name,
            url = 'https://github.com/botcity-dev',
            icon_url = 'https://avatars.githubusercontent.com/u/72993825?s=200&v=4'
        )

        # Defina o rodapé
        mensagem.footer = Footer(
            text = time_read,
            icon_url ='https://avatars.githubusercontent.com/u/1525981?s=200&v=4'
        )

        # Adicione campos extras
        mensagem.fields = [
            Field(name = 'Date: ', value = article_date),
            Field(name = 'Link: ', value = article_link)
        ]

        # Envie a mensagem
        resposta = discord.send_embedded_message(mensagem)

if __name__ == '__main__':
    main()
