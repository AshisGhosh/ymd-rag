import Header from "@/app/components/header";
import ChatSection from "./components/chat-section";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center gap-4 sm:gap-10 p-0 pt-10 sm:p-24 background-gradient">
      <Header />
      <ChatSection />
    </main>
  );
}
