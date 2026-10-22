from typing import Optional
import datetime
import uuid

from sqlalchemy import Boolean, Date, DateTime, ForeignKeyConstraint, Integer, PrimaryKeyConstraint, String, Text, Time, UniqueConstraint, Uuid, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass


class AdminAuth(Base):
    __tablename__ = 'admin_auth'
    __table_args__ = (
        PrimaryKeyConstraint('admin_id', name='admin_auth_pkey'),
        UniqueConstraint('admin_email', name='admin_auth_admin_email_key')
    )

    admin_id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    admin_email: Mapped[str] = mapped_column(String(255), nullable=False)
    admin_password: Mapped[str] = mapped_column(Text, nullable=False)


class JobFair(Base):
    __tablename__ = 'job_fair'
    __table_args__ = (
        PrimaryKeyConstraint('job_fair_id', name='job_fair_pkey'),
    )

    job_fair_id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    job_fair_venue: Mapped[str] = mapped_column(Text, nullable=False)
    jf_gmap_link: Mapped[str] = mapped_column(Text, nullable=False)
    jf_start_time: Mapped[datetime.time] = mapped_column(Time(True), nullable=False)
    jf_end_time: Mapped[datetime.time] = mapped_column(Time(True), nullable=False)
    job_fair_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)

    companies: Mapped[list['Companies']] = relationship('Companies', back_populates='job_fair')
    hr_table: Mapped[list['HrTable']] = relationship('HrTable', back_populates='job_fair')
    job_fair_applicants: Mapped[list['JobFairApplicants']] = relationship('JobFairApplicants', back_populates='job_fair')


class UserAuth(Base):
    __tablename__ = 'user_auth'
    __table_args__ = (
        PrimaryKeyConstraint('user_id', name='user_auth_pkey'),
        UniqueConstraint('user_email', name='user_auth_user_email_key')
    )

    user_id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    user_email: Mapped[str] = mapped_column(String(255), nullable=False)
    user_password: Mapped[str] = mapped_column(Text, nullable=False)

    candidate_details: Mapped[list['CandidateDetails']] = relationship('CandidateDetails', back_populates='user')


class CandidateDetails(Base):
    __tablename__ = 'candidate_details'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['user_auth.user_id'], name='candidate_details_user_id_fkey'),
        PrimaryKeyConstraint('candidate_id', name='candidate_details_pkey')
    )

    candidate_id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    candidate_first_name: Mapped[str] = mapped_column(Text, nullable=False)
    candidate_middle_name: Mapped[str] = mapped_column(Text, nullable=False)
    candidate_last_name: Mapped[str] = mapped_column(Text, nullable=False)
    candidate_disability: Mapped[bool] = mapped_column(Boolean, nullable=False)
    candidate_qr_code: Mapped[str] = mapped_column(Text, nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    candidate_resume: Mapped[Optional[object]] = mapped_column(JSONB)
    candidate_phone_no: Mapped[Optional[str]] = mapped_column(String(15))

    user: Mapped['UserAuth'] = relationship('UserAuth', back_populates='candidate_details')
    job_fair_applicants: Mapped[list['JobFairApplicants']] = relationship('JobFairApplicants', back_populates='candidate')


class Companies(Base):
    __tablename__ = 'companies'
    __table_args__ = (
        ForeignKeyConstraint(['job_fair_id'], ['job_fair.job_fair_id'], name='companies_job_fair_id_fkey'),
        PrimaryKeyConstraint('company_id', name='companies_pkey'),
        UniqueConstraint('job_fair_id', 'company_id', name='companies_job_fair_id_company_id_key')
    )

    company_id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    company_name: Mapped[str] = mapped_column(Text, nullable=False)
    job_fair_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)

    job_fair: Mapped[Optional['JobFair']] = relationship('JobFair', back_populates='companies')
    hr_table: Mapped[list['HrTable']] = relationship('HrTable', back_populates='company')
    job_roles: Mapped[list['JobRoles']] = relationship('JobRoles', back_populates='company')


class HrTable(Base):
    __tablename__ = 'hr_table'
    __table_args__ = (
        ForeignKeyConstraint(['company_id'], ['companies.company_id'], name='hr_table_company_id_fkey'),
        ForeignKeyConstraint(['job_fair_id'], ['job_fair.job_fair_id'], name='hr_table_job_fair_id_fkey'),
        PrimaryKeyConstraint('table_id', name='hr_table_pkey'),
        UniqueConstraint('table_id', 'company_id', 'job_fair_id', name='hr_table_table_id_company_id_job_fair_id_key')
    )

    table_id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    hr_name: Mapped[str] = mapped_column(Text, nullable=False)
    hr_email: Mapped[str] = mapped_column(Text, nullable=False)
    hr_phone_no: Mapped[str] = mapped_column(Text, nullable=False)
    hr_password: Mapped[str] = mapped_column(Text, nullable=False)
    company_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    job_fair_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)

    company: Mapped['Companies'] = relationship('Companies', back_populates='hr_table')
    job_fair: Mapped['JobFair'] = relationship('JobFair', back_populates='hr_table')


class JobFairApplicants(Base):
    __tablename__ = 'job_fair_applicants'
    __table_args__ = (
        ForeignKeyConstraint(['candidate_id'], ['candidate_details.candidate_id'], name='job_fair_applicants_candidate_id_fkey'),
        ForeignKeyConstraint(['job_fair_id'], ['job_fair.job_fair_id'], name='job_fair_applicants_job_fair_id_fkey'),
        PrimaryKeyConstraint('applicant_id', name='job_fair_applicants_pkey'),
        UniqueConstraint('job_fair_id', 'candidate_id', name='job_fair_applicants_job_fair_id_candidate_id_key')
    )

    applicant_id: Mapped[str] = mapped_column(Text, primary_key=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=text('now()'))
    job_fair_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    candidate_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)

    candidate: Mapped[Optional['CandidateDetails']] = relationship('CandidateDetails', back_populates='job_fair_applicants')
    job_fair: Mapped[Optional['JobFair']] = relationship('JobFair', back_populates='job_fair_applicants')


class JobRoles(Base):
    __tablename__ = 'job_roles'
    __table_args__ = (
        ForeignKeyConstraint(['company_id'], ['companies.company_id'], name='job_roles_company_id_fkey'),
        PrimaryKeyConstraint('job_role_id', name='job_roles_pkey'),
        UniqueConstraint('job_role_id', 'company_id', name='job_roles_job_role_id_company_id_key')
    )

    job_role_id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    job_role_name: Mapped[str] = mapped_column(Text, nullable=False)
    vacancy: Mapped[int] = mapped_column(Integer, nullable=False)
    company_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)

    company: Mapped[Optional['Companies']] = relationship('Companies', back_populates='job_roles')