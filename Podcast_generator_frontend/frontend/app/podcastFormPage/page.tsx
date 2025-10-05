"use client";
import React, { useEffect } from "react";
import Cookies from "js-cookie";
import { useRouter } from "next/navigation";
import PodcastForm from "../components/PodcastForm";

export default function PodcastFormProtectedPage() {
  const router = useRouter();
  useEffect(() => {
    const token = Cookies.get("token");
    console.log(token);
    if (!token) {
      console.log("No token found");
      router.replace("/login");
    }
  }, [router]);
  return <PodcastForm />;
}
