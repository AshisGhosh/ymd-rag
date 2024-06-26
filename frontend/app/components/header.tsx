import Image from "next/image";

export default function Header() {
  return (
    <div className="z-10 max-w-5xl w-full items-center justify-between font-mono text-sm lg:flex">
      <p className="fixed left-0 top-0 flex sm:w-full justify-center sm:border-b border-gray-300 bg-gradient-to-b from-zinc-200 p-2 sm:pb-6 sm:pt-8 backdrop-blur-2xl dark:border-neutral-800 dark:bg-zinc-800/30 dark:from-inherit lg:static lg:w-auto  lg:rounded-xl lg:border lg:bg-gray-200 lg:p-4 lg:dark:bg-zinc-800/30">
        Ask questions about Yongmudo and get answers from the chat bot.
      </p>
      <div className="fixed bottom-0 left-0 flex h:24 sm:h-48 w-full items-end justify-center bg-gradient-to-t from-white via-white dark:from-black dark:via-black lg:static lg:h-auto lg:w-auto lg:bg-none">
        <a
          href="https://www.yongmudo.org/"
          className="flex items-center justify-center font-nunito text-lg font-bold gap-2"
        >
          <span>Yongmudo Chat Bot</span>
          <Image
            className="rounded-xl"
            src="/yongmudo.png"
            alt="Yongmudo Logo"
            width={40}
            height={40}
            priority
          />
        </a>
      </div>
    </div>
  );
}
