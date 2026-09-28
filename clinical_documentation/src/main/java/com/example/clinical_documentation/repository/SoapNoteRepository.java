package com.example.clinical_documentation.repository;

import com.example.clinical_documentation.entity.SoapNote;

import org.springframework.data.jpa.repository.JpaRepository;

public interface SoapNoteRepository extends JpaRepository<SoapNote, Long> {

}