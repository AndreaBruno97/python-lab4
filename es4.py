from telegram.ext import Updater, Filters, CommandHandler, MessageHandler
import sys
import pymysql

def start(bot, update):
    update.message.reply_text("Hello!")

def showTasks(bot, update):
    conn = pymysql.connect(user='root', password='root',
                                     host='localhost', database='')
    sql="select todo from es4.tasks"
    cursor = conn.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()

    if len(result)==0:
        update.message.reply_text("Nothing to do, here!")
    else:
        update.message.reply_text(sorted(result))
    cursor.close()
    conn.close()

def newTask(bot, update, args):
    new=" ".join(args)
    conn = pymysql.connect(user='root', password='root',
                           host='localhost', database='')
    sql = "insert into es4.tasks(todo) values (%s)"
    cursor = conn.cursor()
    cursor.execute(sql, (new,))
    conn.commit()
    cursor.close()
    conn.close()
    update.message.reply_text("Task added")

def removeTask(bot, update, args):
    old=" ".join(args)

    conn = pymysql.connect(user='root', password='root',
                           host='localhost', database='')
    sql = "select todo from es4.tasks where todo=%s"
    cursor = conn.cursor()
    cursor.execute(sql,(old,))
    result = cursor.fetchall()
    cursor.close()
    if len(result)>0:
        sql = "delete from es4.tasks where todo=%s"
        cursor = conn.cursor()
        cursor.execute(sql, (old,))
        conn.commit()
        cursor.close()
        update.message.reply_text("Element removed")
    else:
        update.message.reply_text("No such element")
    conn.close()

def removeAllTasks(bot, update, args):
    sub=" ".join(args)

    conn = pymysql.connect(user='root', password='root',
                           host='localhost', database='')
    sql = "select todo from es4.tasks"
    cursor = conn.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()

    if len(result) == 0:
        update.message.reply_text("No element removed")
    else:
        sql = "delete from es4.tasks where todo like %s"
        cursor = conn.cursor()
        sub="%"+sub+"%"
        cursor.execute(sql, (sub,))
        conn.commit()
        cursor.close()
        update.message.reply_text("Elements removed successfully")

    conn.close()

def main():

    updater=Updater(sys.argv[1])
    dp=updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("showTasks", showTasks))
    dp.add_handler(CommandHandler("newTask", newTask, pass_args=True))
    dp.add_handler(CommandHandler("removeTask", removeTask, pass_args=True))
    dp.add_handler(CommandHandler("removeAllTasks", removeAllTasks, pass_args=True))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()